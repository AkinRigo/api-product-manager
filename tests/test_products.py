def create_category(client):
    response = client.post("/categories/", json={"name": "Categoria de teste"})
    assert response.status_code == 201
    return response.json()["id"]


def create_product(client, category_id, **overrides):
    dados = {
        "name": "Produto de teste",
        "sku": "PROD-TESTE-001",
        "price": 25.50,
        "category_id": category_id,
        "min_stock": 5,
    }
    dados.update(overrides)
    return client.post("/products/", json=dados)


def test_create_product_with_category(client):
    category_id = create_category(client)

    response = create_product(client, category_id)

    assert response.status_code == 201
    assert response.json()["category_id"] == category_id
    assert response.json()["stock_quantity"] == 0


def test_reject_duplicate_sku(client):
    category_id = create_category(client)
    assert create_product(client, category_id).status_code == 201

    response = create_product(
        client,
        category_id,
        name="Outro produto",
    )

    assert response.status_code == 409


def test_reject_negative_price(client):
    category_id = create_category(client)

    response = create_product(client, category_id, price=-1)

    assert response.status_code == 422


def test_zero_price_is_allowed(client):
    category_id = create_category(client)

    response = create_product(client, category_id, price=0)

    assert response.status_code == 201


def test_product_can_be_inactivated(client):
    category_id = create_category(client)
    product = create_product(client, category_id).json()

    update_response = client.patch(
        f"/products/{product['id']}",
        json={"is_active": False},
    )
    assert update_response.status_code == 200
    assert update_response.json()["is_active"] is False

    get_response = client.get(f"/products/{product['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["is_active"] is False


def test_list_low_stock_products(client):
    category_id = create_category(client)
    low_stock_product = create_product(
        client,
        category_id,
        sku="PROD-LOW-001",
        min_stock=5,
    ).json()
    regular_product = create_product(
        client,
        category_id,
        sku="PROD-OK-001",
        min_stock=0,
    ).json()
    stock_response = client.post(
        "/stock/",
        json={
            "product_id": regular_product["id"],
            "movement_type": "ENTRY",
            "quantity": 10,
            "reason": "Reposição",
        },
    )
    assert stock_response.status_code == 201

    response = client.get("/products/?low_stock=true")

    assert response.status_code == 200
    product_ids = {product["id"] for product in response.json()}
    assert low_stock_product["id"] in product_ids
    assert len(product_ids) == 1
