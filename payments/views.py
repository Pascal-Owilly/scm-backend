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

base_url = 'https://api.finserve.africa/'
endpoint = 'authentication/api/v3/authenticate/merchant'
full_url = urljoin(base_url, endpoint)

# print(f'Making Jenga API request to URL: {full_url}')
# print(f"Request URL: {api_url}")
# print(f"Request Headers: {headers}")
# print(f"Request Payload: {payload}")
# print(f"Response Status Code: {response.status_code}")
# print(f"Response Body: {response.json()}")

# print(f"Concatenated Data: {data_to_sign}")
# print(f"Private Key Path: {private_key_path}")
# print(f"Signature Base64: {sign_base64}")

# Function to generate the Bearer token
def generate_bearer_token(api_key, merchant_code, consumer_secret):
    # Jenga authentication endpoint URL
    auth_url = "https://uat.finserve.africa/authentication/api/v3/authenticate/merchant"

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Api-Key": api_key,
    }

    # Request payload
    data = {
        "merchantCode": merchant_code,
        "consumerSecret": consumer_secret,
    }

    # Make the request to obtain the Bearer token
    response = requests.post(auth_url, headers=headers, data=json.dumps(data))

    # Handle the response
    if response.status_code == 200:
        # Extract Bearer token from the response
        bearer_token = response.json().get("accessToken")
        return bearer_token
    else:
        return None

# Function to generate the Jenga signature
def generate_signature(data, private_key_path):
    # Load private key from file
    private_key = False
    with open(private_key_path, "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    # Create SHA-256 digest of the data
    message = data.encode('utf-8')
    digest = SHA256.new()
    digest.update(message)

    # Sign the digest with the private key
    signer = PKCS1_v1_5.new(private_key)
    sig_bytes = signer.sign(digest)

    # Encode the signature in base64
    sign_base64 = b64encode(sig_bytes)
    return sign_base64

# Function to make Equity Bank payment
def make_equity_bank_payment(breader_trade, bearer_token, private_key_path):
    # Generate the signature for the Equity Bank request
    signature = generate_signature(f"{breader_trade.breeder.first_name} {breader_trade.breeder.last_name}1450160649886", private_key_path)


    if os.getenv('DEBUG_PRINT_URL', False):
        print(f"Request URL: {api_url}")

    if os.getenv('DEBUG_PRINT_HEADERS', False):
        print(f"Request Headers: {headers}")

    if os.getenv('DEBUG_PRINT_PAYLOAD', False):
        print(f"Request Payload: {payload}")
    # Define the Equity Bank API endpoint and request headers
    api_url = 'https://uat.finserve.africa/v3-apis/transaction-api/v3.0/remittance/internalBankTransfer'
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json',
        'signature': signature.decode('utf-8'),  # Decode from bytes to string
    }

    # Prepare the payload using data from the BreaderTrade model
    payload = {
        "source": {
            "countryCode": "KE",
            "name": f"{breader_trade.breeder.first_name} {breader_trade.breeder.last_name}",
            "accountNumber": "1450160649886"  # Replace with the actual field name
        },
        "destination": {
            "type": "bank",
            "countryCode": "KE",
            "name": "Abattoir",  # Replace with the actual name
            "accountNumber": "1100194977404"  # Replace with the actual account number
        },
        "transfer": {
            "type": "EFT",
            "amount": str(breader_trade.price),  # Assuming price is the payment amount
            "currencyCode": "KES",
            "reference": str(breader_trade.id),  # Using trade ID as reference
            "date": str(breader_trade.transaction_date),
            "description": f"Payment for {breader_trade.breeds_supplied} {breader_trade.breed}"
        }
    }

    # Make the API request
    response = requests.post(api_url, headers=headers, json=payload)
    print(response.json())  # Log or print the entire Jenga API response

    # Check the response status and handle accordingly
    if response.status_code == 200:
        jenga_response = response.json()
        
        # Extract relevant information from Jenga response
        transaction_id = jenga_response['data']['transactionId']
        jenga_status = jenga_response['data']['status']

        # Check Jenga status and update your local model accordingly
        if jenga_status == 'SUCCESS':
            # Create a payment record in the local database
            EquityBankPayment.objects.create(
                breeder_trade=breader_trade,
                amount=breader_trade.price,
                reference_number=jenga_response.get('reference', ''),
                transaction_id=transaction_id,
                payment_method='Equity Bank',
                payment_status='completed',
                payer_name=f"{breader_trade.breeder.first_name} {breader_trade.breeder.last_name}",
                payer_email=breader_trade.breeder.email,
                payment_description=f"Payment for {breader_trade.breeds_supplied} {breader_trade.breed}"
            )
            
            # Update the payment status in your local model
            breader_trade.payment_status = 'completed'
            breader_trade.save()

            return JsonResponse({'message': 'Payment successful', 'transaction_id': transaction_id})
        else:
            # Handle payment failure from Jenga
            return JsonResponse({'message': f'Payment failed. Jenga status: {jenga_status}'}, status=400)
    else:
        # Handle other response statuses
        return JsonResponse({'message': f'Payment failed. Status code: {response.status_code}'}, status=response.status_code)

# Function to request payment
def request_payment(request, breader_trade_id):
    breader_trade = get_object_or_404(BreaderTrade, pk=breader_trade_id)

    # Check if payment has already been requested or completed
    if breader_trade.payment_status != 'pending':
        return JsonResponse({'message': 'Payment already requested or completed'}, status=400)

    # Use getattr(settings, 'JENGA_MERCHANT_CODE'), getattr(settings, 'JENGA_CONSUMER_SECRET'), and getattr(settings, 'JENGA_API_KEY') wherever needed
    merchant_code = getattr(settings, 'JENGA_MERCHANT_CODE')
    consumer_secret = getattr(settings, 'JENGA_CONSUMER_SECRET')
    api_key = getattr(settings, 'JENGA_API_KEY')
    private_key_path = "privatekey.pem"


    # Make the Jenga authentication request to obtain the Bearer token
    bearer_token = generate_bearer_token(api_key, merchant_code, consumer_secret)

    if bearer_token:
        # Make the Equity Bank payment request with the obtained Bearer token
        make_equity_bank_payment(breader_trade, bearer_token, private_key_path)
        return JsonResponse({'message': 'Payment successful'})
    else:
        return JsonResponse({'message': 'Failed to obtain Bearer token'}, status=500)
