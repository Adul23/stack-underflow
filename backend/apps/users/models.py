# Python imports
from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Django imports
from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ImageField,
)
from django.utils.translation import gettext_lazy as _

from apps.abstract.models import AbstractBaseModel

# Project imports
from apps.users.validators import check_domain_name


class CustomUserManager(BaseUserManager):
    """
    Custom User Manager for Creating a Custom Users
    """

    def _obtain_user_instance(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, Any]
    ) -> "CustomUser":
        """Get Custom User instance"""
        if not email:
            raise ValidationError(message=_("Email field is required"))

        if not first_name:
            raise ValidationError(message=_("First name is required"))

        if not last_name:
            raise ValidationError(message=_("Last name is required"))

        new_user: "CustomUser" = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs
        )

        return new_user

    def create_user(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, Any]
    ) -> "CustomUser":
        """
        Create CustomUser model
        """

        new_user: "CustomUser" = self._obtain_user_instance(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **kwargs
        )

        new_user.set_password(password)
        new_user.save(using=self.db)

        return new_user

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **kwargs: dict[str, Any]
    ) -> "CustomUser":
        """
        Create a custom super user
        """

        new_user: "CustomUser" = self._obtain_user_instance(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )

        new_user.set_password(password)
        new_user.save(using=self.db)

        return new_user


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """
    Custom User over existing user model
    """

    EMAIL_MAX_LENGTH = 254
    FIRST_NAME_MAX_LENGTH = 50
    LAST_NAME_MAX_LENGTH = 50
    PASSWORD_MAX_LENGTH = 254
    SUPPORTED_LANGUAGES = [
        ("en", "English"),
        ("ru", "Russian"),
        ("kk", "Kazakh"),
    ]

    email = EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        db_index=True,
        validators=[check_domain_name],
        verbose_name=_("Email Address"),
        help_text=_("User's email address"),
    )

    first_name = CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        verbose_name=_("User first name"),
    )

    last_name = CharField(
        max_length=LAST_NAME_MAX_LENGTH, verbose_name=_("User last name")
    )

    password = CharField(
        max_length=PASSWORD_MAX_LENGTH,
        validators=[validate_password],
        verbose_name=_("User encrypted password"),
    )

    # True if the user can make the requests to the backend
    is_active = BooleanField(
        default=True,
        verbose_name=_("Active status"),
        help_text=_("True if the user is active and has an access to request the data"),
    )

    # True if the user has admin rights
    is_staff = BooleanField(
        default=False,
        verbose_name=_("Staff status"),
        help_text=_("True if user is part of company"),
    )


    avatar = ImageField(blank=True, null=True, verbose_name=_("User avatar"))

    preffered_language = CharField(
        max_length=10,
        choices=SUPPORTED_LANGUAGES,
        default="en",
        verbose_name=_("Preferred language"),
    )

    timezone = CharField(max_length=50, default="UTC", verbose_name=_("User timezone"))

    created_at = DateTimeField(auto_now_add=True, null=True)
    updated_at = DateTimeField(auto_now=True, null=True)
    deleted_at = DateTimeField(null=True, blank=True)

    REQUIRED_FIELDS = ["last_name", "first_name"]
    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        """Meta options for CustomUser"""

        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")
        ordering = ["-created_at"]
