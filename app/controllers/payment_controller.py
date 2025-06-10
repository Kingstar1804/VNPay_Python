import hashlib
import hmac
from urllib.parse import urlencode
from flask import Blueprint, request, redirect, render_template, current_app
from app.data.product_data import product
import datetime
import random, string

payment_bp = Blueprint('payment', __name__)

# Hàm tạo chữ ký HMAC SHA512
def hmac_sha512(key, data):
    return hmac.new(key.encode(), data.encode(), hashlib.sha512).hexdigest()

@payment_bp.route('/pay', methods=['GET', 'POST'])
def pay():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        amount = int(request.form.get('amount')) * 100  # Nhân 100 theo yêu cầu của VNPAY

        vnp_url = current_app.config['VNPAY_URL']
        return_url = current_app.config['VNPAY_RETURN_URL']
        tmn_code = current_app.config['VNPAY_TMN_CODE']
        secret_key = current_app.config['VNPAY_HASH_SECRET']

        input_data = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': tmn_code,
            'vnp_Amount': str(amount),
            'vnp_CurrCode': 'VND',
            'vnp_TxnRef': order_id,
            'vnp_OrderInfo': f'Thanh toan don hang {order_id}',
            'vnp_OrderType': 'other',
            'vnp_Locale': 'vn',
            'vnp_ReturnUrl': return_url,
            'vnp_IpAddr': '127.0.0.1',
            'vnp_CreateDate': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        }

        # Bước 1: Sắp xếp theo key alphabet
        sorted_data = sorted(input_data.items())
        query_string = urlencode(sorted_data)
        
        # Bước 2: Tạo chữ ký
        secure_hash = hmac_sha512(secret_key, query_string)

        # Bước 3: Tạo URL thanh toán đầy đủ
        payment_url = f"{vnp_url}?{query_string}&vnp_SecureHash={secure_hash}"

        return redirect(payment_url)
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return render_template('payment_view.html',  product=product, order_id=order_id)

@payment_bp.route('/payment_return')
def payment_return():
    input_data = request.args.to_dict()
    received_secure_hash = input_data.pop('vnp_SecureHash', None)
    secret_key = current_app.config['VNPAY_HASH_SECRET']

    # Bỏ các key không tham gia vào tính hash
    input_data.pop('vnp_SecureHashType', None)

    # Sắp xếp lại và tạo lại chữ ký
    sorted_data = sorted(input_data.items())
    query_string = urlencode(sorted_data)
    calculated_hash = hmac_sha512(secret_key, query_string)

    if received_secure_hash == calculated_hash:
        return render_template('result.html', response=input_data)
    else:
        return "Xác thực chữ ký thất bại!", 400
