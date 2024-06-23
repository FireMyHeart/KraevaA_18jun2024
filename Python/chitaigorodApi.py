import requests


token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIwOTI3Mzg3LCJpYXQiOjE3MTkxNTM2NzksImV4cCI6MTcxOTE1NzI3OSwidHlwZSI6MjB9.nmp9Ao94NxJGBxss5ijmqU7n3Dv9vn421Z1eYkT-CZw'
class chitaigorodApi:
    def __init__(self, url):
        self.url = url

    def find_book(self, phrase, cityid=12):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.get(self.url+f'v2/search/product?customerCityId={cityid}&phrase={phrase}&products%5Bpage%5D=1&products%5Bper-page%5D=48&sortPreset=relevance', headers=my_headers)
        id = resp.json()["included"][0]["attributes"]["id"]
        price = resp.json()["included"][0]["attributes"]["price"]
        return {"id": id, "price": price}

    def add_to_cart(self, id):
        body = {
            "id": id,
            "adData": {"item_list_name": "product-page"}
        }
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        requests.post(self.url+'v1/cart/product/', json = body, headers=my_headers)

    def get_short_cart(self):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.get(self.url+'v1/cart/short', headers=my_headers)
        return resp.json()["data"]
    
    def get_cart(self):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.get(self.url+'v1/cart/', headers=my_headers)
        return resp.json()
    
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
    
    def delete_book(self, id):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.delete(self.url+f'v1/cart/product/{id}', headers=my_headers)
        return resp.status_code
    
    def delete_all(self):
        my_headers = {}
        my_headers['Authorization'] = f"Bearer {token}"
        resp = requests.delete(self.url+f'v1/cart/', headers=my_headers)
