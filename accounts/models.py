from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO

User = get_user_model()

# def resize_image(image, max_size):
#     # Open the image using PIL
#     img = Image.open(image)

#     # Check if the image size exceeds the maximum limit
#     if image.size > max_size:
#         # Calculate the new dimensions to resize the image while maintaining aspect ratio
#         width, height = img.size
#         aspect_ratio = width / height
#         new_width = int((max_size * aspect_ratio) ** 0.5)
#         new_height = int(max_size / (aspect_ratio ** 0.5))

#         # Resize the image
#         img = img.resize((new_width, new_height), Image.ANTIALIAS)

#         # Save the resized image back to the same BytesIO object
#         img_io = BytesIO()
#         img.save(img_io, format='JPEG')
#         img_io.seek(0)

#         # Update the image file with the resized image
#         image.file = img_io

# def validate_image(image):
#     # Define the allowed file extensions and size limit
#     allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
#     max_size = 1024 * 1024  # 1 MB in bytes

#     # Get the file extension
#     file_extension = image.name.split('.')[-1].lower()

#     # Check if the file extension is valid
#     if file_extension not in allowed_extensions:
#         raise ValidationError("Invalid file extension. Supported extensions: jpg, jpeg, png, gif")

#     # Check if the file size exceeds the limit
#     if image.size > max_size:
#         # Resize the image to fit within the size limit
#         resize_image(image, max_size)

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
