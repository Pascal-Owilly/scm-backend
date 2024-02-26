# utils.py
import requests
import json
import base64
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from django.conf import settings
from transaction.models import BreaderTrade  
from datetime import datetime
import pytz

import random
import string

import logging

logger = logging.getLogger(__name__)

def generate_valid_reference():
    length = random.randint(12, 20)
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def generate_equity_bank_bearer_token(api_key, merchant_code, consumer_secret):
    auth_url = "https://uat.finserve.africa/authentication/api/v3/authenticate/merchant"

    headers = {
        "Content-Type": "application/json",
        "Api-Key": api_key,
    }

    # print('HEADERS', headers)

    data = {
        "merchantCode": merchant_code,
        "consumerSecret": consumer_secret,
    }
    # print('DATA', data)

    response = requests.post(auth_url, headers=headers, data=json.dumps(data))
    print("Bearer Token Generation Response:", response.status_code, response.json())

    # expiration_time_str = "2023-07-13T07:03:02Z"
    # expiration_time_utc = datetime.fromisoformat(expiration_time_str.rstrip("Z"))
    # expiration_time_utc = expiration_time_utc.replace(tzinfo=pytz.utc)

    # Convert to your local time zone
    # local_time_zone = pytz.timezone("Africa/Nairobi")  # Replace with your time zone
    # expiration_time_local = expiration_time_utc.astimezone(local_time_zone)

    # # Convert to a human-readable format
    # human_readable_expiration_time = expiration_time_local.strftime("%Y-%m-%d %H:%M:%S %Z")
    # print("Human-readable expiration time in local time:", human_readable_expiration_time)
    if response.status_code == 200:
        bearer_token = response.json().get("accessToken")
        return bearer_token
    else:
        logger.error("Failed to generate bearer token. Status code: %d, Response: %s", response.status_code, response.text)

        return None

    # Example usage:
    merchant_code = getattr(settings, 'JENGA_MERCHANT_CODE')
    consumer_secret = getattr(settings, 'JENGA_CONSUMER_SECRET')
    api_key = getattr(settings, 'JENGA_API_KEY')

    bearer_token_response = generate_equity_bank_bearer_token(api_key, merchant_code, consumer_secret)

    if bearer_token_response and "refreshToken" in bearer_token_response:
        refresh_token = bearer_token_response["refreshToken"]
        print("Refresh Token:", refresh_token)

        # Use the bearer_token as needed
        print("NEW BEARER TOKEN:", bearer_token)
    else:
        print("Failed to generate bearer token")
    
def generate_equity_bank_signature(breeder_trade):
    # Load the private key from the file
    private_key_path = "privatekey.pem"
    with open(private_key_path, "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    # Create the data to be signed
    signature_data = f"{breeder_trade.seller.account_number}{str(breeder_trade.price)}{settings.CURRENCY_CODE}{breeder_trade.reference}"
    print('Signature Data before encoding:', signature_data)

    # Sign the data using the private key
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new()
    digest.update(signature_data.encode('utf-8'))
    signature = signer.sign(digest)
    print('Signature Data after encoding:', signature)

    # Base64 encode the signature
    signature_base64 = base64.b64encode(signature).decode('utf-8')

    return signature_base64
    
def make_equity_bank_transfer_request(breeder_trade, access_token, signature):
    # Replace with actual logic to make the Equity Bank transfer request
    # This involves constructing the request payload based on the example provided

    # Endpoint for making the transfer request
    transfer_url = "https://uat.finserve.africa/v3-apis/transaction-api/v3.0/remittance/internalBankTransfer"

    # Request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "signature": signature
    }

    print("Bearer Token:", access_token)

    # Request payload
    payload = {
    "source": {
        "countryCode": "KE",  
        "name": breeder_trade.seller.user.username,  
        "accountNumber": breeder_trade.seller.account_number  
    },
    "destination": {
        "type": "bank",
        "countryCode": "KE",  
        "name": f"{breeder_trade.breeder.first_name} {breeder_trade.breeder.last_name}",  
        "accountNumber": breeder_trade.bank_account_number
    },
    "transfer": {
        "type": "EFT",
        "amount": str(breeder_trade.price),
        "currencyCode": settings.CURRENCY_CODE,  
        "reference": breeder_trade.reference,  # Replace with a function to generate a valid reference
        "date": breeder_trade.transaction_date.strftime('%Y-%m-%d'),  
        "description": f"Payment from {breeder_trade.abattoir.user.username} to {breeder_trade.breeder.first_name} {breeder_trade.breeder.last_name}"
    }
}

    # print('Transfer Request Payload:', payload)


    # Convert payload to JSON
    payload_json = json.dumps(payload)
    # print('Transfer Request JSON Payload:', payload_json)

    # Make the request
    # Before making the request
    # print("Access Token:", access_token)
    # print("Transfer Request Payload:", payload)
    # print("Transfer Request Headers:", headers)

    response = requests.post(transfer_url, headers=headers, data=payload_json)
    response_data = response.json()
    print("Transfer Request Headers: %s", headers)
    print("Transfer Request Payload: %s", payload)
    print("Transfer Response Data: %s", response_data)
    print("Transfer Response Data after request: %s", response_data)


    # after making request
    print("Transfer Response Data after request:", response_data)

    return response_data
