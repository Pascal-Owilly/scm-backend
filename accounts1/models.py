from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    current_city = models.CharField(max_length=50, blank=True, null=True, default=None)  # Allowing null values
    profile_pic = models.ImageField(
        upload_to='profile_pics',
        default='default.png',
        blank=True,
        null=False,
        # validators=[validate_image],
    )
    bio = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
