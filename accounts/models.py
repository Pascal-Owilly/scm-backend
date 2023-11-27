from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='John')
    last_name = models.CharField(max_length=255, default='John')
    phone_number = models.CharField(max_length=20, null=False, blank=False, default=12345678910)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics',
        default='default.png',
        blank=True,
        null=False,
        # validators=[validate_image],
    )

    def __str__(self):
        return self.user.email

