from chitaigorodApi import chitaigorodApi


api = chitaigorodApi('https://web-gate.chitai-gorod.ru/api/')

# Добавление одного товара в корзину
def test_1():
    id = api.find_book('Удивительная девочка')["id"]
    api.add_to_cart(id)
    id_aded = api.get_short_cart()["items"][0]

    delid = api.get_cart()["products"][0]["id"]
    api.delete_book(delid)

    assert id == id_aded

# Изменение количества единиц одного товара в корзине
def test_2():
    id = api.find_book('Удивительная девочка')["id"]
    api.add_to_cart(id)
    cart_id = api.get_cart()["products"][0]["id"]
    new_q = 4
    q_in_cart = api.change_quantity_of_book(cart_id, new_q)

    api.delete_book(cart_id)

    assert new_q == q_in_cart

# Удаление товара из корзины
def test_3():
    id = api.find_book('Удивительная девочка')["id"]
    api.add_to_cart(id)
    del_id = api.get_cart()["products"][0]["id"]
    result = api.delete_book(del_id)
    null_cart = api.get_short_cart()["quantity"]
    assert len(api.get_short_cart()["items"]) == 0
    assert null_cart == 0
    assert result == 204

# Добавление нескольких товаров в корзину
def test_4():
    books = ['1986', 'Сумерки', 'Цветы для Элджернона']
    total_cost = 0
    for i in books:
        id = api.find_book(i)["id"]
        total_cost += api.find_book(i)["price"]
        api.add_to_cart(id)
    api.get_short_cart()
    count = len(api.get_short_cart()["items"])
    total_sum = api.get_cart()["costWithSale"]

    api.delete_all()

    assert total_sum == total_cost
    assert count == len(books)
