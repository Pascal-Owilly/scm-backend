from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from .models import CustomUser, UserProfile
from rest_framework import status

from .serializers import CustomUserSerializer, LogoutSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

class GetUserRole(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            # Get the user's role from the CustomUser model
            user_role = request.user.role
            return Response({"role": user_role})
        else:
            return Response({"role": "anonymous"}, status=status.HTTP_401_UNAUTHORIZED)


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
            'community': user.community,  
            'country': user.country, 
            'head_of_family':user.head_of_family,
            'country': user.country,
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