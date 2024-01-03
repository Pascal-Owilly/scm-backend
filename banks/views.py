from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Status, Bank, BankBranch, Payment, BankUser, Financier, FinancierUser
from transaction.models import BreaderTrade
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from decouple import config
from django.core.exceptions import ObjectDoesNotExist
from custom_registration.models import CustomUser
from .serializers import (
    StatusSerializer,
    BankSerializer,
    BankBranchSerializer,
    PaymentSerializer,
    BankUserSerializer,
    FinancierSerializer,
    FinancierUserSerializer,
)

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class BankBranchViewSet(viewsets.ModelViewSet):
    queryset = BankBranch.objects.all()
    serializer_class = BankBranchSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class BankUserViewSet(viewsets.ModelViewSet):
    queryset = BankUser.objects.all()
    serializer_class = BankUserSerializer

class FinancierViewSet(viewsets.ModelViewSet):
    queryset = Financier.objects.all()
    serializer_class = FinancierSerializer

class FinancierUserViewSet(viewsets.ModelViewSet):
    queryset = FinancierUser.objects.all()
    serializer_class = FinancierUserSerializer
    
# Payments

def initiate_payments(request, breeder_trade_id):
    try:
        # Assuming you have the breeder trade instance and related objects
        breeder_trade = BreaderTrade.objects.get(pk=breeder_trade_id)
        breeder_user = breeder_trade.breeder
        bank_instance = breeder_trade.bank
        bank_branch_instance = breeder_trade.bank_branch
        teller_user = breeder_trade.teller

        # Check if the breeder trade is pending payment
        if breeder_trade.payment_status == 'pending':
            # Create a new payment instance
            payment = Payment.objects.create(
                payment_code='1234',
                amount=breeder_trade.price,
                breeder_trade=breeder_trade,
                national_id=breeder_user.id_number,
                mobile_number=breeder_user.mobile_number,
                breeder_id=breeder_user,
                bank_id=bank_instance,
                bank_branch_id=bank_branch_instance,
                teller_id=teller_user,
                status_id=Status.objects.get(is_dormant=False)
            )

            # Print information about the payment
            print(f"Payment successful for breeder {breeder_user.first_name} {breeder_user.last_name}")
            print(f"Amount: {payment.amount}")
            print(f"Payment Code: {payment.payment_code}")
            print(f"Transaction Date: {payment.payment_initiation_date}")


            # Update BreederTrade and Status
            breeder_trade.payment_status = 'completed'
            breeder_trade.save()

            # Update Status
            status_instance = payment.status_id
            status_instance.is_dormant = False
            status_instance.save()

            # Send Email Notifications
            send_mail(
                'Payment Confirmation',
                'Your payment has been successfully processed.',
                'pascaouma54@gmail.com',
                [breeder_user.email],
                fail_silently=False,
            )

            send_mail(
                'Payment Confirmation',
                'A payment has been made to a breeder.',
                'owillypascal@gmail.com',
                [teller_user.email, 'pascaouma55@gmail.com'],
                fail_silently=False,
            )

            messages.success(request, 'Payment successful!')
        else:
            messages.warning(request, 'Payment has already been made for this trade.')

    except BreaderTrade.DoesNotExist:
        messages.error(request, 'Breeder trade not found.')

    return JsonResponse({'status': 'success', 'message': 'Payment successful!'})
