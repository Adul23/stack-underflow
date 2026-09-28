# Python imports
from typing import Any, Optional

from django.contrib.auth.password_validation import validate_password

# Django imports
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Rest-Framework imports
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    EmailField,
    IntegerField,
    ListField,
    Serializer,
)
from rest_framework.serializers import (
    ValidationError as DRFValidationError,
)

# Project imports
from apps.users.models import CustomUser


class UserLoginResponseSerializer(Serializer):
    """Serializer for user login response"""

    id = IntegerField()
    first_name = CharField()
    last_name = CharField()
    email = EmailField()
    access = CharField()
    refresh = CharField()

    class Meta:
        fields = ("id", "first_name", "last_name", "email", "access", "refresh")


class UserLoginFailSerializer(Serializer):
    """Serializer for user login error"""

    email = ListField(child=CharField(), required=False)
    password = ListField(child=CharField(), required=False)

    class Meta:
        fields = ("email", "password")


class HTTP405MethodNowAllowedSerializer(Serializer):
    """Serializer for 405 HTTP method"""

    detail = CharField()

    class Meta:
        fields = ("detail",)


class UserLoginSerializer(Serializer):
    """Serializer for user login"""

    email = EmailField(required=True, max_length=CustomUser.EMAIL_MAX_LENGTH)
    password = CharField(required=True, max_length=CustomUser.PASSWORD_MAX_LENGTH)

    class Meta:
        fields = ("email", "password")

    def validate_email(self, value: str) -> str:
        return value.lower()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validates input data"""
        email: str = attrs["email"]
        password: str = attrs["password"]

        user: Optional[CustomUser] = CustomUser.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                {
                    "email": _("User with this email %(email)s does not exist")
                    % {"email": email}
                }
            )

        if not user.check_password(raw_password=password):
            raise ValidationError({"password": _("Incorrect password")})

        attrs["user"] = user
        return super().validate(attrs)


class UserRegisterResponseSerializer(Serializer):
    """Serializer for user register response"""

    id = IntegerField()
    first_name = CharField()
    last_name = CharField()
    email = EmailField()

    class Meta:
        fields = ("id", "first_name", "last_name", "email")


class UserRegisterFailSerializer(Serializer):
    """Serializer for user register error"""

    email = ListField(child=CharField(), required=False)
    password = ListField(child=CharField(), required=False)
    first_name = CharField()
    last_name = CharField()

    class Meta:
        fields = ("first_name", "last_name", "email", "password")


class UserRegisterSerializer(Serializer):
    """Serializer for custom user registration"""

    first_name = CharField(required=True, max_length=CustomUser.FIRST_NAME_MAX_LENGTH)
    last_name = CharField(required=True, max_length=CustomUser.LAST_NAME_MAX_LENGTH)
    email = EmailField(required=True, max_length=CustomUser.EMAIL_MAX_LENGTH)
    password = CharField(required=True, max_length=CustomUser.PASSWORD_MAX_LENGTH)

    class Meta:
        fields = ["first_name", "last_name", "email", "password"]

    def validate_email(self, value: str) -> str:
        value = value.lower()
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError(
                message=_(f"This email address {value} already exist")
            )
        return value

    def validate_password(self, value: str) -> str:
        try:
            validate_password(value)
        except ValidationError as e:
            raise ValidationError(list(e.messages))
        return value


class UserLanguageUpdateSerializer(Serializer):
    """Serializer for updating user's preferred language"""

    language = ChoiceField(choices=CustomUser.SUPPORTED_LANGUAGES, required=True)
    label = _("Preferred Language")

    class Meta:
        fields = ("language",)

    def validate_language(self, value: str) -> str:
        if value not in dict(CustomUser.SUPPORTED_LANGUAGES):
            raise DRFValidationError(_("Unsupported language choice"))
        return value


class UserTimezoneUpdateSerializer(Serializer):
    """Serializer for updating user's preferred time zone"""

    timezone = CharField(required=True, max_length=50)
    label = _("Preferred Time Zone")

    class Meta:
        fields = ("timezone",)
