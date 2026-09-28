# Django imports
from drf_spectacular.utils import OpenApiResponse, inline_serializer
from rest_framework import serializers

error_response = inline_serializer(
    name="ErrorResponse",
    fields={"detail": serializers.CharField()},
)

validation_error_response = inline_serializer(
    name="ValidationErrorResponse",
    fields={
        "detail": serializers.CharField(required=False),
        "name": serializers.ListField(child=serializers.CharField(), required=False),
    },
)

ERROR_400 = OpenApiResponse(response=error_response, description="Bad request.")
ERROR_401 = OpenApiResponse(response=error_response, description="Unauthorized.")
ERROR_403 = OpenApiResponse(response=error_response, description="Forbidden.")
ERROR_404 = OpenApiResponse(response=error_response, description="Not found.")
ERROR_429 = OpenApiResponse(response=error_response, description="Too many requests.")
VALIDATION_400 = OpenApiResponse(
    response=validation_error_response, description="Validation error."
)
