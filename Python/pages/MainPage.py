from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class MainPage:
    def __init__(self, driver):
        self._driver = driver
        self._driver.get("https://www.chitai-gorod.ru/")
        self._driver.implicitly_wait(15)
        self._driver.find_element(By.CSS_SELECTOR, 'div.button.change-city__button.change-city__button--accept.blue').click()
        driver.maximize_window()
    
    def cookies(self, cookie):
        self._driver.add_cookie(cookie)
        self._driver.refresh()

    def enter_values(self, key):
        try:
            self._driver.find_element(By.CSS_SELECTOR, 'button.header-search__clear').click()
        except Exception:
            pass
        self._driver.find_element(By.CSS_SELECTOR, 'input[enterkeyhint="search"]').send_keys(key, Keys.RETURN)
       
    def add_to_cart(self):
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='__layout']/div/div[3]/div[1]/div/div/div[1]/section/section/div/article[1]/div[3]/div/span[contains(text(),'Купить')]"))
        )
        title = self._driver.find_element(By.CSS_SELECTOR, 'div.product-title__head').text
        price = self._driver.find_element(By.CSS_SELECTOR, 'div.product-price__value.product-price__value--discount').text.strip().split(' ', 1)[0]
        button = self._driver.find_element(By.CSS_SELECTOR, 'div.button.action-button.blue')
        self._driver.execute_script("arguments[0].click();", button)
        return {"title": title, "price": price}
    
    def go_cart(self):
        self._driver.find_element(By.CSS_SELECTOR, 'a.header-cart.sticky-header__controls-item').click()
    
    def check_book(self):
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-title__head'))
        )
        return self._driver.find_element(By.CSS_SELECTOR, 'div.product-title__head').text
    
    def change_quantity(self, qntt):
        self._driver.find_element(By.CSS_SELECTOR, 'input[type="number"]').send_keys(Keys.BACKSPACE)
        #self._driver.find_element(By.CSS_SELECTOR, 'input[type="number"]').clear()
        self._driver.find_element(By.CSS_SELECTOR, 'input[type="number"]').send_keys(qntt, Keys.RETURN)
    
    def check_quantity(self, text):
        WebDriverWait(self._driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'div.info-item__title'), text)
            # EC.presence_of_element_located((By.CSS_SELECTOR, 'div.info-item__value'))
        )
        q = self._driver.find_element(By.CSS_SELECTOR, 'div.info-item__title').text
        result = q.split(' ', 1)[0]
        return result
    
    def del_book(self):
        self._driver.find_element(By.CSS_SELECTOR, 'button.button.cart-item__actions-button.cart-item__actions-button--delete').click()
    
    def check_total(self):
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cart-sidebar__info-summary > div > div.info-item__value'))
        )
        total = self._driver.find_element(By.CSS_SELECTOR, 'div.cart-sidebar__info-summary > div > div.info-item__value').text.strip()
        total = total.replace(' ', '')[:-1]
        return total
        