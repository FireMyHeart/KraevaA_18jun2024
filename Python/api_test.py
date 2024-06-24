from chitaigorodApi import chitaigorodApi
import allure

api = chitaigorodApi('https://web-gate.chitai-gorod.ru/api/')


@allure.id("SKYPRO-1")
@allure.epic("Корзина Читай-город. API")
@allure.story("Добавление товара в корзину")
@allure.feature("ADD")
@allure.title("Добавление одной книги в корзину")
@allure.severity("blocker")
@allure.suite("API тесты на работу с корзиной")
def test_1():
    id = api.find_book('Удивительная девочка')["id"]
    api.add_to_cart(id)
    id_aded = api.get_short_cart()["items"][0]
    with allure.step("Очистка тестового пространства: удаление книги из корзины"):
        delid = api.get_cart()["products"][0]["id"]
        api.delete_book(delid)
    with allure.step("Проверить, что id книги в корзине совпадает с id книги, которую добавляли в корзину"):
        assert id == id_aded

@allure.id("SKYPRO-2")
@allure.epic("Корзина Читай-город. API")
@allure.story("Изменение количества товаров в корзине")
@allure.feature("UPDATE")
@allure.title("Увеличение количества единиц одной книги в корзине")
@allure.severity("critical")
@allure.suite("API тесты на работу с корзиной")
def test_2():
    id = api.find_book('Удивительная девочка')["id"]
    api.add_to_cart(id)
    cart_id = api.get_cart()["products"][0]["id"]
    new_q = 4
    q_in_cart = api.change_quantity_of_book(cart_id, new_q)
    with allure.step("Очистка тестового пространства: удаление книги из корзины"):
        api.delete_book(cart_id)
    with allure.step("Проверить, что число единиц книг изменилось в соответствии с установленным значением"):
        assert new_q == q_in_cart

@allure.id("SKYPRO-3")
@allure.epic("Корзина Читай-город. API")
@allure.story("Удаление товара из корзины")
@allure.feature("DELETE")
@allure.title("Удаление одной книги из корзины")
@allure.severity("blocker")
@allure.suite("API тесты на работу с корзиной")
def test_3():
    id = api.find_book('Удивительная девочка')["id"]
    api.add_to_cart(id)
    del_id = api.get_cart()["products"][0]["id"]
    result = api.delete_book(del_id)
    null_cart = api.get_short_cart()["quantity"]
    with allure.step("Проверить, что список книг в корзине после удаления пуст"):
        assert len(api.get_short_cart()["items"]) == 0
    with allure.step("Проверить, что количество книг равно нулю"):
        assert null_cart == 0
    with allure.step("Проверить, статус-код ответа - 204"):
        assert result == 204

@allure.id("SKYPRO-4")
@allure.epic("Корзина Читай-город. API")
@allure.story("Добавление нескольких товаров в корзину")
@allure.feature("ADD")
@allure.title("Добавление 3 книг в корзину")
@allure.severity("critical")
@allure.suite("API тесты на работу с корзиной")
def test_4():
    with allure.step("Добавить в корзину все книги из списка"):
        books = ['Настольная игра Каркассон, Hobby World', 'Настольная игра Большая бродилка', 'Акриловая белая краска olki, 100 мл']
        total_cost = 0
        for i in books:
            id = api.find_book(i)["id"]
            price = api.find_book(i)["price"]
            total_cost += api.find_book(i)["price"]
            api.add_to_cart(id)
    api.get_short_cart()
    with allure.step("Посчитать количество книг в корзине"):
        count = len(api.get_short_cart()["items"])
    with allure.step("Посчитать общую сумму книг в корзине"):
        total_sum = api.get_cart()["costWithSale"]
    api.delete_all()
    with allure.step("Проверить, что общая сумма покупки совпадает с общей стоимостью трех добавленных книг"):
        assert total_sum == total_cost
    with allure.step("Проверить, что количество книг в корзине совпадает с количеством добавленных книг"):
        assert count == len(books)
