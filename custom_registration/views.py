from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import CustomUser, UserProfile, Payment, BankTeller, CustomerService
from rest_framework import status

from .serializers import CustomUserSerializer, LogoutSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer, CustomerServiceSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import RoleSerializer, PaymentSerializer
from django.template.loader import render_to_string  # Add this import
from django.utils.html import strip_tags
from django.core.mail import send_mail
from transaction.models import BreaderTrade

from .models import PasswordReset
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


class GetUserRole(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            # Get the user's role from the CustomUser model
            user_role = request.user.role
            return Response({"role": user_role})
        else:
            return Response({"role": "anonymous"}, status=status.HTTP_401_UNAUTHORIZED)

class RoleListView(APIView):
    def get(self, request, *args, **kwargs):
        # Replace this with your logic to fetch roles from the database or any other source
        roles = ['buyer', 'no_role', 'warehouse_personnel']

        serializer = RoleSerializer(data={'roleChoices': roles})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Extract the role data from the request
        role_data = request.data.get('roleChoices', {})

        # Perform validation and update logic
        # This is a placeholder, replace it with your actual logic to update roles in the database
        # You may need to iterate through the roles and update the corresponding user's role in the database
        updated_roles = role_data.get('roleChoices', [])
        
class CustomTokenRefreshView(TokenRefreshView):
    # Customize if needed
    '''
    this automatically refreshes the token
    '''
    pass

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # Replace with your custom serializer


class CustomUserRegistrationViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        from custom_registration.serializers import CustomUserSerializer  # Import here to break the circular import

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Assign a role to the user, replace 'default_role' with your logic
            user.role = 'No role'  # Replace with your logic for assigning roles
            user.save()


            # Refresh token after saving the user instance
            refresh = RefreshToken.for_user(user)

            tokens = {'refresh': str(refresh), 'access': str(refresh.access_token)}
            return Response({'user': {'id': user.id, 'username': user.username}, 'tokens': tokens}, status=200)
        return Response(serializer.errors, status=400)

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"detail": "No account found with this email"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a password reset token and send it via email
            token = default_token_generator.make_token(user)
            reset_instance = PasswordReset.objects.create(user=user, token=token)

            # Obtain uidb64 from the user instance
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))


            # Construct reset link
            reset_url = reverse_lazy('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            # Compose email message
            subject = 'Password Reset Request'
            context = {
                'password_reset_url': reset_url,
            }

            message = render_to_string('password_reset_email.html', context)
            plain_message = strip_tags(message)
            from_email = 'pascalouma54@gmail.com'  # Replace with your email
            to_email = [user.email]

            send_mail(subject, plain_message, from_email, to_email, html_message=message)

            return Response({"detail": "Check your email for password reset link "}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
            reset_instance = PasswordReset.objects.get(user=user, token=token)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist, PasswordReset.DoesNotExist):
            return Response({"detail": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            # Set the new password and delete the reset instance
            user.set_password(new_password)
            user.save()
            reset_instance.delete()

            return Response({"detail": "Password reset successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        # Retrieve the UserProfile instance associated with the authenticated user
        return self.request.user.userprofile

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'detail': 'User profile deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# List all profiles

class UserProfilesListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()  # Assuming you have a UserProfile model

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class CustomUserLoginViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate username and password
        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=400)

        try:
            # Authenticate the user
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=400)

        # Check the password
        if not user.check_password(password):
            return Response({'error': 'Invalid credentials.'}, status=400)

        # # If authentication is successful, generate tokens
        
        # If authentication is successful, generate tokens
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)

        tokens = {
            'refresh': str(refresh),
            'access': str(access),
        }

        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'bank_account_number': user.bank_account_number,
            'email': user.email,
            'community': user.community,  
            'county': user.county, 
            'head_of_family':user.head_of_family,
            'county': user.county,
            'groups': user.groups,
            'role': user.role,  
        }

        return Response({'user': {'id': user.id, 'username': user.username}, 'tokens': tokens}, status=200)

class CustomLogoutViewSet(viewsets.ViewSet):
    
    def create(self, request, *args, **kwargs):
        # Perform any additional actions you need before logging out
        # For example, invalidate the user's token if you're using token-based authentication

        # Logout the user
        response = LogoutView.as_view()(request, *args, **kwargs)

        # Return a JSON response using the LogoutSerializer
        serializer = LogoutSerializer(data={'detail': 'Successfully logged out.'})
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

# Payment

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract the 'id' from the request data
        breeder_trade_id = request.data.get('id')

        try:
            # Get the corresponding BreaderTrade instance
            breeder_trade = BreaderTrade.objects.get(pk=breeder_trade_id)
        except BreaderTrade.DoesNotExist:
            # Handle the case where the BreaderTrade instance doesn't exist
            return Response({'error': 'BreaderTrade instance does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the payment and associate it with the BreaderTrade instance
        payment = serializer.save(breeder_trade=breeder_trade)

        # Additional logic related to payment creation can be performed here
        # For example, generate payment code, send confirmation email, etc.

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list_payments(self, request, *args, **kwargs):
        # Retrieve all payments
        payments = self.get_queryset()
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    def process_payment(self):
        # Example: Update payment status to 'Paid'
        self.status = 'payment_initiated'
        self.save()

        # Add additional payment processing logic here
        # For example, interact with a payment gateway, log payment details, etc.

        # Return True if the payment was successful
        return True

    @action(detail=True, methods=['post'])
    def process_payment_and_notify_breeder(self, request, *args, **kwargs):
        instance = self.get_object()

        # Additional logic related to payment details can be performed here
        # For example, check payment status, update related models, log information, etc.

        # Assume the Breeder model has a 'name' field
        breeder_first_name = instance.breeder_trade.breeder.first_name
        breeder_last_name = instance.breeder_trade.breeder.last_name
        breeder_name = f"{breeder_first_name} {breeder_last_name}"

        # Perform the payment processing (replace with your actual payment processing logic)
        success = instance.process_payment()

        if success:
            # Send email to breeder about payment and breeder trade status
            subject = f"Payment and Breeder Trade Code - {instance.payment_code}"

            # Add breeder's name to the context
            context = {
                'payment': instance,
                'success_message': 'You will receive the payment once the processing is complete.',
                'breeder_name': breeder_name,
                'price': instance.breeder_trade.price,
                'payment_initiation_date': instance.payment_initiation_date,
            }

            message = render_to_string('payment_and_breeder_trade_status_email_template.html', context)
            plain_message = strip_tags(message)
            from_email = 'pascalouma54@gmail.com'
            to_email = [instance.breeder_trade.breeder.email]

            send_mail(subject, plain_message, from_email, to_email, html_message=message)

            # Serialize the payment data and return the response
            serializer = self.get_serializer(instance)

            # Additional logic to send emails to BankTeller and CustomerService
            # Replace the following lines with your actual email sending logic

            # Send email to BankTeller
            bank_teller_emails = BankTeller.objects.values_list('user__email', flat=True)
            bank_teller_subject = 'Bank Teller Notification'

            # Add payment code to the context
            bank_teller_context = {
                'payment': instance,
                'success_message': 'Payment has been initiated. Please review the details.',
                'payment_code': instance.payment_code,
            }

            # Use bank teller email template
            bank_teller_message = render_to_string('bank_teller_status_email_template.html', bank_teller_context)

            send_mail(bank_teller_subject, strip_tags(bank_teller_message), from_email, bank_teller_emails, html_message=bank_teller_message)

            # Send email to CustomerService
            customer_service_emails = CustomerService.objects.values_list('user__email', flat=True)
            customer_service_subject = 'Customer Service Notification'

            # Add relevant context for Customer Service
            customer_service_context = {
                'payment': instance,
                'success_message': 'A new payment has been initiated. Please review the details.',
                'additional_info': 'You may need to take further action based on the payment details.',
            }

            # Use customer service email template
            customer_service_message = render_to_string('customer_service_status_email_template.html', customer_service_context)

            send_mail(customer_service_subject, strip_tags(customer_service_message), from_email, customer_service_emails, html_message=customer_service_message)

            return Response(serializer.data)
        else:
            # Handle payment failure, return an appropriate response
            return Response({'error': 'Payment processing failed'}, status=status.HTTP_400_BAD_REQUEST)

        # Search breeder details by code

    @action(detail=False, methods=['get'])
    def search_payment_by_code(self, request, *args, **kwargs):
        payment_code = request.query_params.get('payment_code')
        if not payment_code:
            return Response({'error': 'Payment code parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Query the database for the payment with the given payment_code
        payment = get_object_or_404(Payment, payment_code=payment_code)
        # Serialize the payment data and return the response
        serializer = self.get_serializer(payment)
        return Response(serializer.data)

class CustomerServiceViewSet(viewsets.ModelViewSet):
    queryset = CustomerService.objects.all()
    serializer_class = CustomerServiceSerializer