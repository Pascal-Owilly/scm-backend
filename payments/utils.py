# utils.py
import requests
import json
import base64
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from django.conf import settings
from transaction.models import BreaderTrade  # Import the BreederTrade model

def generate_equity_bank_bearer_token():
    # Replace with actual logic to retrieve or generate the Equity Bank Bearer Token
    # This might involve making a request to the Equity Bank API to obtain the token
    # Make sure to handle token expiration and refresh logic if necessary

    # Placeholder values, replace with actual implementation
    api_key = getattr(settings, 'JENGA_API_KEY')
    token_url = "https://api.finserve.africa/authentication/api/v3/authenticate/merchant"

    # Headers for token request
    headers = {
        "Content-Type": "application/json",
        "Api-Key": api_key
    }

    print('HEADERS:', headers)


    # Request payload
    data = {
        "merchantCode": getattr(settings, 'JENGA_MERCHANT_CODE'),
        "consumerSecret": getattr(settings, 'JENGA_CONSUMER_SECRET')
    }
    print('DATA:', data)

    try:
        # Make the request
        response = requests.post(token_url, headers=headers, json=data)
        response_data = response.json()

        # Print the entire response
        print('Token API Response:', response_data)

        # Extract and return the access token
        access_token = response_data.get("accessToken")
        print('Access Token:', access_token)

        return access_token

    except Exception as e:
        print('Error retrieving access token:', str(e))
        return None

def generate_equity_bank_signature(breeder_trade):
    # Replace with actual logic to generate the Equity Bank Signature
    # This involves using the private key to sign specific data in the request payload
    # Make sure to follow the signature formula provided in the Equity Bank documentation

    # Load the private key from the file
    private_key_path = "privatekey.pem"
    with open(private_key_path, "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    # Create the data to be signed
    signature_data = f"{breeder_trade.bank_account_number}{breeder_trade.price}{settings.CURRENCY_CODE}{breeder_trade.reference}"
    print('Signature Data:', signature_data)

    # Sign the data using the private key
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new()
    digest.update(signature_data.encode('utf-8'))
    signature = signer.sign(digest)

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

    # Request payload
    payload = {
        "source": {
            "countryCode": "KE",  
            "name": breeder_trade.abattoir.user.username,  
            "accountNumber": breeder_trade.abattoir.account_number  
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
            "reference": breeder_trade.reference,
            "date": breeder_trade.transaction_date.strftime('%Y-%m-%d'),  
            "description": f"Payment from {breeder_trade.abattoir.user.username} to {breeder_trade.breeder.first_name} {breeder_trade.breeder.last_name}"
        }
    }

    print('Transfer Request Payload:', payload)


    # Convert payload to JSON
    payload_json = json.dumps(payload)
    print('Transfer Request JSON Payload:', payload_json)

    # Make the request
    # Before making the request
    print("Access Token:", access_token)
    print("Transfer Request Payload:", payload)
    print("Transfer Request Headers:", headers)

    response = requests.post(transfer_url, headers=headers, data=payload_json)
    response_data = response.json()
    print('Transfer Response Data:', response_data)
    # after making request
    print("Transfer Response Data after request:", response_data)

    return response_data
