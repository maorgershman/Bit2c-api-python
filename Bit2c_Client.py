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

    def query(self, url: str, method: str, parameters: list, data=None):
        
        parmas_string = ""

        if method == "GET":

            for params in parameters:
                parmas_string += params + "&"

            parmas_string += f"nonce={self.nonce}"

            url = f"{self.base_url}{url}?{parmas_string}"
            sign = self.create_hash(parmas_string)

            headers = {
                "Key": self.key,
                "Sign": sign
            }
            res = requests.get(url, headers=headers)
            
            return res

        if method == "POST":
            
            #params to hash should be param1=x&param2=y...&nonce=number
            parmas_string = ""
            data["nonce"] = self.nonce
            url = self.base_url+url
            for param in parameters:
                parmas_string += f"{param}&"
            parmas_string += f"nonce={self.nonce}"

            sign = self.create_hash(parmas_string)
            headers = {
                "Key": self.key,
                "Sign": sign,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            res = requests.post(url, headers=headers, data=data)
            return res

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

