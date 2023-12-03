from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from transaction.models import BreaderTrade, AbattoirPaymentToBreader
from django_daraja.mpesa.core import MpesaClient
import time

class MpesaPaymentView(APIView):
    """
    Endpoint for making M-Pesa payments
    """

    def post(self, request, *args, **kwargs):
        print("MpesaPaymentView is executed")

        breader_trade_id = request.data.get("breader_trade_id")
        user_id = request.data.get('user_id', None)

        if user_id is not None:
            breader_trade = get_object_or_404(BreaderTrade, id=breader_trade_id, user=user_id)
            phone_number = str(breader_trade.phone_number)  
        else:
            return Response({"success": False, "msg": "User ID is not provided"}, status=400)

        amount = int(breader_trade.price)

        cl = MpesaClient()
        account_reference = 'Supplier'
        transaction_desc = 'Supplies'
        callback_url = 'https://mydomain.com/mpesa-payments/daraja/'

        response = self.make_mpesa_payment_with_retry(cl, phone_number, amount, account_reference, transaction_desc, callback_url)

        print("M-Pesa API Response Content:")
        print("mpesa response:", response.content)

        response_data = response.json()

        response_code = response_data.get("ResponseCode")
        response_description = response_data.get("ResponseDescription")

        if response_code == "0" and response_description == "Request successful, please enter your pin to confirm payment":
            payment, created = AbattoirPaymentToBreader.objects.get_or_create(breader_trade=breader_trade)
            payment.amount = amount
            payment.payment_id = response_data.get("CheckoutRequestID")
            payment.save()

            breader_trade.status = "Paid"
            breader_trade.save()
            
            return Response({"success": True, "msg": "M-Pesa payment initiated successfully", "response": response_data}, status=201)
        
        elif response_code == "1032" and response_description == "Request canceled by user.":
            return Response({"success": False, "msg": "User canceled the payment"}, status=400)

        else:
            return Response({"success": False, "msg": "M-Pesa payment initiation failed"}, status=400)

    def make_mpesa_payment_with_retry(self, cl, phone_number, amount, account_reference, transaction_desc, callback_url):
        max_retries = 3
        retry_delay = 20  # 60 seconds

        for retry in range(max_retries):
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            print(f"Attempt {retry + 1} - M-Pesa API Response Content:")
            print(response.content)

            if response.status_code == 200:
                return response
            else:
                print(f"Service is temporarily unavailable. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)

        return None  # Return None if max retries are reached without success