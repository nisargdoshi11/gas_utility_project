# apps/accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True)
    address = models.TextField(_("Address"), blank=True)
    customer_id = models.CharField(_("Customer ID"), max_length=20, unique=True, null=True)
    is_staff_member = models.BooleanField(
        _("Staff Member Status"),
        default=False,
        help_text=_("Designates whether the user can handle service requests."),
    )

    # Customizing the Many-to-Many relationships with related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Added related_name
        blank=True,
        help_text=_("The groups this user belongs to."),
        verbose_name=_("groups"),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Added related_name
        blank=True,
        help_text=_("Specific permissions for this user."),
        verbose_name=_("user permissions"),
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email or self.username
