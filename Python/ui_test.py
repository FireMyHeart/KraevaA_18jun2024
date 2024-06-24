from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from MainPage import MainPage
import allure


cookie = {
    'name': 'access-token',
    'value': 'Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIwOTI3Mzg3LCJpYXQiOjE3MTkyMjY0MjEsImV4cCI6MTcxOTIzMDAyMSwidHlwZSI6MjB9.zgDPLfpa2TtGJRLs1MApo7kJpNz_y-_NuUkS7ATGHOc'
}

@allure.id("SKYPRO-5")
@allure.epic("Корзина Читай-город. UI")
@allure.story("Добавление одного товара в корзину")
@allure.feature("ADD")
@allure.title("Добавление одной книги в корзину")
@allure.description("Добавление 1 книги в корзину с последующим изменением количества ее экземпляров и удалением из корзины")
@allure.severity("critical")
@allure.suite("UI тесты на работу с корзиной")
def test_add_book():
    with allure.step("Создать экземпляр класса и открыть браузер"):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        main_page = MainPage(driver)
        # main_page.cookies(cookie) кукисы не пробрасывались, добавлялся почему-то второй ключ в Application, по факту авторизации нет
    main_page.enter_values("Удивительная девочка")
    with allure.step("Добавить первую книгу из поисковой выдачи в корзину"):
        dct = main_page.add_to_cart()
    main_page.go_cart()
    book = main_page.check_book()
    new_q = '5'
    main_page.change_quantity(new_q)
    cart_q = main_page.check_quantity('5 товаров')
    main_page.del_book()
    clear_cart = main_page.check_quantity('0 товаров')
    with allure.step("Проверить, что в корзину добавилась нужная книга"):
        assert book == dct["title"]
    with allure.step("Проверить, что число экземпляров книги увеличилось в соответствии с выставленным значением"):
        assert cart_q == new_q
    with allure.step("Проверить, книга удалилась из корзины"):
        assert clear_cart == '0'

@allure.id("SKYPRO-6")
@allure.epic("Корзина Читай-город. UI")
@allure.story("Добавление нескольких товаров в корзину")
@allure.feature("ADD")
@allure.title("Добавление 3 книг в корзину")
@allure.description("Добавление книг из списка и подсчет общей стоимости покупки")
@allure.severity("critical")
@allure.suite("UI тесты на работу с корзиной")
def test_add_three_books():
    with allure.step("Создать экземпляр класса и открыть браузер"):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        main_page = MainPage(driver)
        # main_page.cookies(cookie)
    with allure.step("Добаввить по очереди 3 книги в корзину через поиск"):
        total_sum = 0
        with allure.step("Выполнить цикл для поиска каждой книги по названию и последующего добавления в корзину первой книги из поисковой выдачи"):
            for i in ["1984", "Сумерки", "Цветы для Элджернона"]:
                main_page.enter_values(i)
                dct1 = main_page.add_to_cart()
                total_sum += int(dct1["price"])
    with allure.step("Перейти в корзину"):
        main_page.go_cart()
        with allure.step("Записать в переменную общую стоимость покупки"):
            cart_total = main_page.check_total()
    with allure.step("Проверить, что сумма покупки совпадает с общей суммой трех добавленных книг"):
        assert total_sum >= int(cart_total)
