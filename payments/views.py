import json
from django.shortcuts import get_object_or_404
from django.conf import settings  # Import settings module
from django.http import JsonResponse
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from base64 import b64encode
import requests
from transaction.models import BreaderTrade
from payments.models import EquityBankPayment
import logging
from urllib.parse import urljoin
import os
logger = logging.getLogger(__name__)

# base_url = 'https://api.finserve.africa/'
# endpoint = 'authentication/api/v3/authenticate/merchant'
# full_url = urljoin(base_url, endpoint)
# print('full url', full_url)
# Function to generate the Bearer token
# Function to generate the Bearer token
def generate_bearer_token(api_key, merchant_code, consumer_secret):
    auth_url = "https://uat.finserve.africa/v3-apis/transaction-api/v3.0/remittance/internalBankTransfer"

    headers = {
        "Content-Type": "application/json",
        "Api-Key": api_key,
    }

    data = {
        "merchantCode": merchant_code,
        "consumerSecret": consumer_secret,
    }

    response = requests.post(auth_url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        bearer_token = response.json().get("accessToken")
        return bearer_token
    else:
        return None


# Function to generate the Jenga signature
def generate_signature(breader_trade, private_key_path):
    # Concatenate values in the specified order
    data_to_sign = f"{breader_trade.breeder.first_name} {breader_trade.breeder.last_name}1450160649886/{breader_trade.transaction_date.strftime('%Y-%m-%d')}"

    private_key = False
    with open(private_key_path, "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    message = data_to_sign.encode('utf-8')
    digest = SHA256.new()
    digest.update(message)

    signer = PKCS1_v1_5.new(private_key)
    sig_bytes = signer.sign(digest)

    # Encode the signature in base64 as a string
    sign_base64 = b64encode(sig_bytes).decode('utf-8')
    return sign_base64


# Function to make Equity Bank payment
def make_equity_bank_payment(breader_trade, bearer_token, private_key_path):
    access_token = bearer_token
    signature = generate_signature(breader_trade, private_key_path)

    api_url = 'https://uat.finserve.africa/v3-apis/transaction-api/v3.0/remittance/internalBankTransfer'
    
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json',
        'signature': signature
    }

    payload = {
        "source": {
            "countryCode": "KE",
            "name": "Abattoir",
            "accountNumber": "1450160649886"  # Replace with the actual source account number
        },
        "destination": {
            "type": "bank",
            "countryCode": "KE",
            "name": f"{breader_trade.breeder.first_name} {breader_trade.breeder.last_name}",
            "accountNumber": "1370169757312"
        },
        "transfer": {
            "type": "EFT",
            "amount": str(breader_trade.price),
            "currencyCode": "KES",
            "reference": str(breader_trade.id),
            "date": str(breader_trade.transaction_date),
            "description": f"Payment for {breader_trade.breeds_supplied} {breader_trade.breed}"
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)

    print(f"Request URL: {api_url}")
    print(f"Request Headers: {headers}")
    print(f"Request Payload: {payload}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

    if response.status_code == 200:
        EquityBankPayment.objects.create(
            breeder_trade=breader_trade,
            amount=breader_trade.price,
            reference_number=response.json().get('reference_number', ''),
            transaction_id=response.json().get('transactionId', ''),  # Updated to use Equity Bank's transactionId
            payment_method='Equity Bank',
            payment_status='SUCCESS'  # Updated to match Equity Bank's status
        )
        breader_trade.payment_status = 'completed'
        breader_trade.save()
        return JsonResponse({'message': 'Payment successful'})
    else:
        return JsonResponse({'message': f'Payment failed. Status code: {response.status_code}'}, status=response.status_code)

# Function to request payment
# Function to request payment
def request_payment(request, breader_trade_id):
    breader_trade = get_object_or_404(BreaderTrade, pk=breader_trade_id)

    if breader_trade.payment_status != 'pending':
        return JsonResponse({'message': 'Payment already requested or completed'}, status=400)

    merchant_code = getattr(settings, 'JENGA_MERCHANT_CODE')
    consumer_secret = getattr(settings, 'JENGA_CONSUMER_SECRET')
    api_key = getattr(settings, 'JENGA_API_KEY')
    private_key_path = "privatekey.pem"  # Replace with the actual path to your private key

    bearer_token = generate_bearer_token(api_key, merchant_code, consumer_secret)

    if bearer_token:
        # Pass the BreaderTrade object to the make_equity_bank_payment function
        make_equity_bank_payment(breader_trade, bearer_token, private_key_path)
        return JsonResponse({'message': 'Payment successful'})
    else:
        return JsonResponse({'message': 'Failed to obtain Bearer token'}, status=500)
