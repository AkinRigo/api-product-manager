def test_create_category_and_list_categories(client):
    create_response = client.post(
        "/categories/",
        json={"name": "Eletrônicos", "description": "Aparelhos e acessórios"},
    )

    assert create_response.status_code == 201

    list_response = client.get("/categories/")

    assert list_response.status_code == 200
    assert any(item["id"] == create_response.json()["id"] for item in list_response.json())


def test_reject_duplicate_category_name(client):
    dados = {"name": "Categoria duplicada"}
    assert client.post("/categories/", json=dados).status_code == 201

    response = client.post("/categories/", json=dados)

    assert response.status_code == 409


def test_category_can_have_products(client):
    category_response = client.post(
        "/categories/",
        json={"name": "Categoria em uso"},
    )
    assert category_response.status_code == 201
    category_id = category_response.json()["id"]

    product_response = client.post(
        "/products/",
        json={
            "name": "Produto vinculado",
            "sku": "PROD-CAT-001",
            "price": 10,
            "category_id": category_id,
        },
    )
    assert product_response.status_code == 201

    assert product_response.json()["category_id"] == category_id
