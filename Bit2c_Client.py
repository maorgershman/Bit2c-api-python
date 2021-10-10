import time
import requests
import hmac
import hashlib
import base64
import logging

#TODO: add logging
#TODO: add docs
#TODO: finish main class

class Bit2c_Client:

    def __init__(self, key: str, secret: str):
        self.key = key
        self.secret = secret
        self.nonce = int(time.time_ns())
        self.base_url = "https://bit2c.co.il/"

    def create_hash(self, hash_key: str):
        sign = base64.b64encode(hmac.new(self.secret.encode(), hash_key.encode(), hashlib.sha512).digest())
        self.nonce+=1
        time.sleep(1)
        return sign

    def query(self, url: str, method: str, params: list):
        # Add the nonce to the parameters list
        params["nonce"] = self.nonce

        # Stringify the parameters list (url encoded style)
        parmas_string = "&".join(params)
        
        # Sign the parameters list and add to the requests header along with the key
        headers = {
            "Key": self.key,
            "Sign": self.create_hash(parmas_string)
        }

        # Concat the url to the base url
        url = f"{self.base_url}{url}"

        if method == "GET":
            # Insert the parameters list into the url
            return requests.get(f"{url}?{parmas_string}", headers=headers)

        if method == "POST":
            # The content type must be urlencoded for some reason, even though we send JSON data
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            return requests.post(url, headers=headers, data=params)

    def fetch_balance(self):

        url = "Account/Balance"

        res = self.query(url, "GET", [])

        with open("json_files/balance.json", "w") as f:
            f.write(res.text)

        return res.text

    def fetch_my_orders(self, pair):

        url = "Order/MyOrders"

        params = [f"pair={pair}"]

        res = self.query(url, "GET", params)

        with open(f"json_files/my_orders_{pair}.json", "w") as f:
            f.write(res.text)

        return res

        url = "Order/GetById"

        params = []

    def fetch_order_by_id(self, id):
        url = "Order/GetById"
        params = [f"id={id}"]

    def fetch_account_history(self, from_time, to_time):
        url = "Order/AccountHistory"
        params = [f"fromTime={from_time}"]
    def fetch_order_history(self):
        url = "Order/OrderHistory"

    def fetch_order_history_by_id(self):
        url = "Order/HistoryByOrderId"

    def add_order(self):
        url = "Order/AddOrder"
    
    def cancel_order(self, id):
        url = "Order/CancelOrder"
        params = [f"id={id}"]
        data = {
            "id": id,
        }
        res = self.query(url, "POST", params, data)
        return res.text

    def buy_market_price(self, total, pair):
        url = "Order/AddOrderMarketPriceBuy"

        params = [f"Total={total}&Pair={pair}"]

        data = {
            "Total": total,
            "Pair": pair
        }

        res = self.query(url, "POST", params, data)
        print(res.text)
    def sell_market_price(self):
        url = "Order/AddOrderMarketPriceSell"

    def add_stop_limit_order(self):
        url = "Order/AddStopOrder"

