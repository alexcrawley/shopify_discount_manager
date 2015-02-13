import requests
import json
import datetime
from bs4 import BeautifulSoup


class ShopifyDiscountManager(object):
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'
    DATE_FORMAT = "%Y-%m-%d"
    DEFAULT_DISCOUNT_TYPE = 'percentage'

    def __init__(self, shopify_shop_name, login_email, password):
        self.SESSION = requests.Session()
        self.CSRF_TOKEN = ''
        self.LOGIN_EMAIL = login_email
        self.PASSWORD = password
        self.SHOPIFY_STORE = shopify_shop_name + '.myshopify.com'
        self.ADMIN_URL = 'https://' + self.SHOPIFY_STORE + '/admin'
        self.LOGIN_URL = self.ADMIN_URL + '/auth/login'
        self.DISCOUNT_URL = self.ADMIN_URL + '/discounts.json'
        self.SHOPIFY_SHOP_NAME = shopify_shop_name

    def create_discount_code(self, **kwargs):
        # Login to shopify, set the csrf token etc
        if not self.CSRF_TOKEN:
            self.login()

        DISCOUNT_KWARGS = {
            'code': 'DEFAULT_CODE',
            'discount_type': self.DEFAULT_DISCOUNT_TYPE,
            'value': 0,
            'minimum_order_amount': 0,
            'usage_limit': None,
            'starts_at': datetime.date.today().strftime(self.DATE_FORMAT),
            'ends_at': None,
            'applies_once': False
        }

        if kwargs:
            DISCOUNT_KWARGS.update(**kwargs)

        DISCOUNT_DICT = {'discount': DISCOUNT_KWARGS}

        # Post to create the discount
        headers = self.get_headers()
        response = self.SESSION.post(
            self.DISCOUNT_URL, data=json.dumps(DISCOUNT_DICT), headers=headers)

        return response

    def disable_discount_code(self, shopify_discount_id):
        if not self.CSRF_TOKEN:
            self.login()

        disable_url = self.ADMIN_URL + '/discounts/' + str(shopify_discount_id) + '/disable'

        headers = self.get_headers()
        response = self.SESSION.post(disable_url, headers=headers)
        return response

    def login(self):
        username = self.LOGIN_EMAIL
        password = self.PASSWORD
        payload = {'login': username, 'password': password}
        headers = {'Shopify-Auth-Mechanisms': 'password'}
        headers['Host'] = self.SHOPIFY_STORE
        headers['User-Agent'] = self.USER_AGENT

        # Post the login data
        response = self.SESSION.post(self.LOGIN_URL, data=payload, headers=headers)

        self.set_token(response.content)

        return response

    def set_token(self, content):
        soup = BeautifulSoup(content)
        auth_token_element = soup.find(
            'input', type='hidden', attrs={'name': 'authenticity_token'})
        authentication_token = auth_token_element['value']
        self.CSRF_TOKEN = authentication_token

    def get_headers(self):
        headers = {'X-CSRF-Token': self.CSRF_TOKEN}
        headers['X-Shopify-Api-Features'] = 'pagination-headers'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        return headers
