import hashlib
import hmac
from urllib.parse import urlencode

class Vnpay:
    def __init__(self):
        self.requestData = {}
        self.responseData = {}

    def get_payment_url(self, base_url, hash_secret):
        query_string = self.get_query_string(self.requestData)
        secure_hash = self.hmac_sha512(hash_secret, query_string)
        return f"{base_url}?{query_string}&vnp_SecureHash={secure_hash}"

    def get_query_string(self, data):
        sorted_data = sorted((k, v) for k, v in data.items() if v)
        return urlencode(sorted_data)

    def hmac_sha512(self, key, data):
        return hmac.new(key.encode(), data.encode(), hashlib.sha512).hexdigest()

    def verify_payment_response(self, response_data, secure_hash, hash_secret):
        response_data = {k: v for k, v in response_data.items() if k != 'vnp_SecureHash' and k != 'vnp_SecureHashType'}
        query_string = self.get_query_string(response_data)
        calculated_hash = self.hmac_sha512(hash_secret, query_string)
        return secure_hash == calculated_hash
