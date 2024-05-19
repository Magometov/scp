from enum import StrEnum

from rest_framework import status


class VerificationResponse(StrEnum):
    SUCCESS = "Successful confirmation."
    EXPIRED = "The reference period has expired. We've sent a new verification link to your email."
    INVALID = "You have sent an invalid token."
    ALREADY_VERIFIED = "You have already verified your account."


VerificationStatusCodes: dict[VerificationResponse, int] = {
    VerificationResponse.SUCCESS: status.HTTP_200_OK,
    VerificationResponse.EXPIRED: status.HTTP_410_GONE,
    VerificationResponse.INVALID: status.HTTP_400_BAD_REQUEST,
    VerificationResponse.ALREADY_VERIFIED: status.HTTP_208_ALREADY_REPORTED,
}
