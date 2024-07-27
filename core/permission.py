from rest_framework import permissions
import logging

class IsVendorOrReadOnly(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated  and (request.user.user_type == "Vendor" or request.user.is_staff):
            return True
        else:
            logging.warning(
                f"Access denied for user {request.user} to perform action {request.method} on {view}."
            )
            return False
  

class IsCustomerOrReadOnly(permissions.BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated  and (request.user.user_type == "Customer" or request.user.is_staff):
            return True
        else:
            logging.warning(
                f"Access denied for user {request.user} to perform action {request.method} on {view}."
            )
            return False
  

class IsAdminOrReadOnly(permissions.BasePermission):
  message = "You do not have permission to perform this action."
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    if request.user and request.user.is_staff:
      return True
    else:
      logging.warning(
      f"Access denied for user {request.user} to perform action {request.method} on {view}.")
      return False