from django.shortcuts import render
from django.http import JsonResponse
from transaction.models import BreaderTrade
from .utils import generate_equity_bank_bearer_token, generate_equity_bank_signature, make_equity_bank_transfer_request
from django.conf import settings

def make_payment(request, breeder_trade_id):
    try:
        # Retrieve the BreederTrade object
        breeder_trade = BreaderTrade.objects.get(pk=breeder_trade_id)

        merchant_code = getattr(settings, 'JENGA_MERCHANT_CODE')
        consumer_secret = getattr(settings, 'JENGA_CONSUMER_SECRET')
        api_key = getattr(settings, 'JENGA_API_KEY')

        # Generate Equity Bank Bearer Token
        access_token = generate_equity_bank_bearer_token(api_key, merchant_code, consumer_secret)
        print('ACCESS TOKEN', access_token)
        # Generate Equity Bank Signature
        signature = generate_equity_bank_signature(breeder_trade)

        # Make Equity Bank Transfer Request
        response_data = make_equity_bank_transfer_request(breeder_trade, access_token, signature)

        # Process the response and update the BreaderTrade model
        if response_data.get("status"):
            breeder_trade.payment_status = "completed"
            breeder_trade.save()
            return JsonResponse({"message": "Payment successful"}, status=200)
        else:
            return JsonResponse({"message": "Payment failed"}, status=400)

    except BreaderTrade.DoesNotExist:
        return JsonResponse({"message": "BreaderTrade not found"}, status=404)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)
