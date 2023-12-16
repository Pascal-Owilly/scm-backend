# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
# from accounts.models import Profile

# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False

# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline, )
#     list_display = ('username', 'email', 'first_name', 'last_name', 'profile_username')

#     def profile_username(self, obj):
#         # Check if the profile exists and has a user associated with it
#         if hasattr(obj, 'profile') and obj.profile.user:
#             return obj.profile.user.username
#         return ''

#     profile_username.short_description = 'Profile Username'

# # Re-register the UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
