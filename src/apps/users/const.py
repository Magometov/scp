from enum import StrEnum

from rest_framework import status


class VerificationResponse(StrEnum):
    SUCCESS = "Successful confirmation."
    ALREADY_VERIFIED = "You have already verified your account."
    EXPIRED = "The reference period has expired. We've sent a new verification link to your email."
    INVALID = "You have sent an invalid token."
    MISSING_TOKEN = "You have not provided a token."


VerificationStatusCodes: dict[VerificationResponse, int] = {
    VerificationResponse.SUCCESS: status.HTTP_200_OK,
    VerificationResponse.ALREADY_VERIFIED: status.HTTP_208_ALREADY_REPORTED,
    VerificationResponse.EXPIRED: status.HTTP_410_GONE,
    VerificationResponse.INVALID: status.HTTP_422_UNPROCESSABLE_ENTITY,
    VerificationResponse.MISSING_TOKEN: status.HTTP_400_BAD_REQUEST,
}
