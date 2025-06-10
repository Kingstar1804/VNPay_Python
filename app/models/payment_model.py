from vnpay import Vnpay
from flask import current_app
import datetime

def create_payment_url(order_id, amount, bank_code=''):
    vnp = Vnpay()
    vnp.requestData = {
        'vnp_Version': '2.1.0',
        'vnp_Command': 'pay',
        'vnp_TmnCode': current_app.config['VNPAY_TMN_CODE'],
        'vnp_Amount': int(amount) * 100,
        'vnp_CurrCode': 'VND',
        'vnp_TxnRef': order_id,
        'vnp_OrderInfo': f'Thanh toan don hang {order_id}',
        'vnp_OrderType': 'other',
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': current_app.config['VNPAY_RETURN_URL'],
        'vnp_IpAddr': '127.0.0.1',
        'vnp_CreateDate': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
    }
    if bank_code:
        vnp.requestData['vnp_BankCode'] = bank_code
    payment_url = vnp.get_payment_url(
        current_app.config['VNPAY_URL'],
        current_app.config['VNPAY_HASH_SECRET']
    )
    return payment_url
