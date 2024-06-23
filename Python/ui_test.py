from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.MainPage import MainPage


cookie = {
    'name': 'access-token',
    'value': 'Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIwOTI3Mzg3LCJpYXQiOjE3MTkwODY0MDksImV4cCI6MTcxOTA5MDAwOSwidHlwZSI6MjB9.BFZKDjdbFwzFRmmx-qgE66KX_Th2xo2ZFtZTDZUTgt0'
}

def test_add_book():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    main_page = MainPage(driver)
    # main_page.cookies(cookie) кукисы не пробрасывались, добавлялся почему-то второй ключ в Application, по факту авторизации нет
    main_page.enter_values("Удивительная девочка")
    dct = main_page.add_to_cart()
    main_page.go_cart()
    book = main_page.check_book()
    new_q = '5'
    main_page.change_quantity(new_q)
    cart_q = main_page.check_quantity('5 товаров')
    main_page.del_book()
    clear_cart = main_page.check_quantity('0 товаров')
    assert book == dct["title"]
    assert cart_q == new_q
    assert clear_cart == '0'

def test_add_three_books():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    main_page = MainPage(driver)
    main_page.cookies(cookie)
    total_sum = 0
    for i in ["1984", "Сумерки", "Цветы для Элджернона"]:
        main_page.enter_values(i)
        dct1 = main_page.add_to_cart()
        total_sum += int(dct1["price"])
    main_page.go_cart()
    cart_total = main_page.check_total()
    assert str(total_sum) == cart_total
