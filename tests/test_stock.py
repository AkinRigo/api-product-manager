from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest


def create_product(client, sku="PROD-STOCK-001"):
    category_response = client.post(
        "/categories/",
        json={"name": "Categoria de estoque"},
    )
    assert category_response.status_code == 201

    product_response = client.post(
        "/products/",
        json={
            "name": "Produto de estoque",
            "sku": sku,
            "price": 10,
            "category_id": category_response.json()["id"],
        },
    )
    assert product_response.status_code == 201
    return product_response.json()


def create_movement(client, product_id, movement_type, quantity, reason):
    return client.post(
        "/stock/",
        json={
            "product_id": product_id,
            "movement_type": movement_type,
            "quantity": quantity,
            "reason": reason,
        },
    )


def test_entry_exit_and_adjustment_update_stock(client):
    product = create_product(client)

    entry = create_movement(
        client, product["id"], "ENTRY", 10, "Reposição de estoque"
    )
    assert entry.status_code == 201
    assert entry.json()["stock_before"] == 0
    assert entry.json()["stock_after"] == 10
    assert entry.json()["reason"] == "Reposição de estoque"

    exit_movement = create_movement(
        client, product["id"], "EXIT", 3, "Venda"
    )
    assert exit_movement.status_code == 201
    assert exit_movement.json()["stock_before"] == 10
    assert exit_movement.json()["stock_after"] == 7
    assert exit_movement.json()["reason"] == "Venda"

    adjustment = create_movement(
        client, product["id"], "ADJUSTMENT", 4, "Contagem física"
    )
    assert adjustment.status_code == 201
    assert adjustment.json()["stock_before"] == 7
    assert adjustment.json()["stock_after"] == 4
    assert adjustment.json()["reason"] == "Contagem física"

    product_response = client.get(f"/products/{product['id']}")
    assert product_response.status_code == 200
    assert product_response.json()["stock_quantity"] == 4

    zero_adjustment = create_movement(
        client, product["id"], "ADJUSTMENT", 0, "Estoque contado zerado"
    )
    assert zero_adjustment.status_code == 201
    assert zero_adjustment.json()["stock_before"] == 4
    assert zero_adjustment.json()["stock_after"] == 0
    assert client.get(f"/products/{product['id']}").json()["stock_quantity"] == 0


def test_adjustment_requires_reason(client):
    product = create_product(client)

    response = client.post(
        "/stock/",
        json={
            "product_id": product["id"],
            "movement_type": "ADJUSTMENT",
            "quantity": 0,
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize("movement_type", ["ENTRY", "EXIT"])
def test_regular_movement_does_not_require_reason(client, movement_type):
    product = create_product(client)
    if movement_type == "EXIT":
        entry = create_movement(client, product["id"], "ENTRY", 1, None)
        assert entry.status_code == 201

    response = client.post(
        "/stock/",
        json={
            "product_id": product["id"],
            "movement_type": movement_type,
            "quantity": 1,
        },
    )

    assert response.status_code == 201
    assert response.json()["reason"] is None


def test_reject_exit_when_stock_is_insufficient(client):
    product = create_product(client)

    response = create_movement(
        client, product["id"], "EXIT", 1, "Saída sem saldo"
    )

    assert response.status_code == 409
    product_response = client.get(f"/products/{product['id']}")
    assert product_response.json()["stock_quantity"] == 0


@pytest.mark.parametrize("movement_type", ["ENTRY", "EXIT"])
def test_inactive_product_rejects_regular_movements(client, movement_type):
    product = create_product(client)
    if movement_type == "EXIT":
        entry = create_movement(
            client, product["id"], "ENTRY", 2, "Saldo inicial"
        )
        assert entry.status_code == 201

    update_response = client.patch(
        f"/products/{product['id']}",
        json={"is_active": False},
    )
    assert update_response.status_code == 200

    response = create_movement(
        client, product["id"], movement_type, 1, "Movimentação de teste"
    )

    assert response.status_code == 409


def test_concurrent_exits_do_not_create_negative_stock(client):
    product = create_product(client)
    entry = create_movement(
        client, product["id"], "ENTRY", 5, "Saldo para concorrência"
    )
    assert entry.status_code == 201

    barrier = Barrier(2)

    def send_exit():
        barrier.wait()
        return create_movement(
            client, product["id"], "EXIT", 5, "Saída concorrente"
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        responses = list(executor.map(lambda _: send_exit(), range(2)))

    assert sorted(response.status_code for response in responses) == [201, 409]

    product_response = client.get(f"/products/{product['id']}")
    assert product_response.status_code == 200
    assert product_response.json()["stock_quantity"] == 0
