import os

class Config:
    VNPAY_TMN_CODE = 'BY0W0IUG'  # Mã Website VNPAY
    VNPAY_HASH_SECRET = 'XKV7ACKUPNX58O22SEO551MLJG5LGPD2'
    VNPAY_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
    VNPAY_RETURN_URL = 'http://localhost:5000/payment_return'
