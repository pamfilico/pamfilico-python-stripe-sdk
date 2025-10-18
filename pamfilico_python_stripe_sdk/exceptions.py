"""Custom exceptions for Stripe SDK operations."""


class StripeSDKException(Exception):
    """Base exception for all Stripe SDK errors."""

    def __init__(self, message: str, original_error: Exception | None = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class StripeAuthenticationError(StripeSDKException):
    """Raised when Stripe API authentication fails."""
    pass


class StripeAPIError(StripeSDKException):
    """Raised when Stripe API returns an error."""
    pass


class StripeInvalidRequestError(StripeSDKException):
    """Raised when request to Stripe API is invalid."""
    pass


class StripeValidationError(StripeSDKException):
    """Raised when input validation fails."""
    pass
