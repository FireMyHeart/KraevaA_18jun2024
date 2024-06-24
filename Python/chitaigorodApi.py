import requests
import allure

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIwOTI3Mzg3LCJpYXQiOjE3MTkyMjY0MjEsImV4cCI6MTcxOTIzMDAyMSwidHlwZSI6MjB9.zgDPLfpa2TtGJRLs1MApo7kJpNz_y-_NuUkS7ATGHOc'
class chitaigorodApi:
    def __init__(self, url):
        self.url = url

    @allure.step("Найти книги по названию {phrase}")
    def find_book(self, phrase, cityid=12):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.get(self.url+f'v2/search/product?customerCityId={cityid}&phrase={phrase}&products%5Bpage%5D=1&products%5Bper-page%5D=48&sortPreset=relevance', headers=my_headers)
        id = resp.json()["included"][0]["attributes"]["id"]
        price = resp.json()["included"][0]["attributes"]["price"]
        return {"id": id, "price": price}

    @allure.step("Добавить первую книгу по id {id} в корзину")
    def add_to_cart(self, id):
        body = {
            "id": id,
            "adData": {"item_list_name": "product-page"}
        }
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        requests.post(self.url+'v1/cart/product/', json = body, headers=my_headers)

    @allure.step("Получить список id книг в корзине")
    def get_short_cart(self):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.get(self.url+'v1/cart/short', headers=my_headers)
        return resp.json()["data"]
    
    @allure.step("Получить список книг в корзине с подробной информацией")
    def get_cart(self):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.get(self.url+'v1/cart/', headers=my_headers)
        return resp.json()
    
    @allure.step("Изменить количество экземпляров {number} книги по id {id}")
    def change_quantity_of_book(self, id, number):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        body = [
            {
                "id": id,
                "quantity": number
            }
        ]
        resp = requests.put(self.url+'v1/cart/', json = body, headers=my_headers)
        return resp.json()["products"][0]["quantity"]
    
    @allure.step("Удалить книгу по id {id} из корзины")
    def delete_book(self, id):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.delete(self.url+f'v1/cart/product/{id}', headers=my_headers)
        return resp.status_code
    
    @allure.step("Очистить корзину")
    def delete_all(self):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.delete(self.url+f'v1/cart/', headers=my_headers)
