# # myapp/permissions.py

# from rest_framework import permissions

# class HasGroupPermission(permissions.BasePermission):
#     def __init__(self, required_group):
#         self.required_group = required_group

#     def has_permission(self, request, view):
#         # Check if the user has the required group permission
#         return request.user.groups.filter(name=self.required_group).exists()
