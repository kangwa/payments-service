from pydantic import SecretStr


def mask_api_key(full_key: str) -> str:
    """Create a masked version of an API key for safe logging/display.

    Args:
        full_key: The complete API key to mask.

    Returns:
        A string containing the first 4 and last 4 characters of the key,
        with "..." in between. For example: "abcd...wxyz".

    Example:
        >>> key = "abcdefghijklmnop"
        >>> masked = mask_api_key(key)
        >>> print(masked)  # Output: "abcd...mnop"
    """
    return f"{full_key[:4]}...{full_key[-4:]}"


class StrongSecret(SecretStr):
    """Enhanced SecretStr for handling sensitive string data.

    Extends Pydantic's SecretStr to provide additional validation and security
    features for handling sensitive data like API keys and tokens.

    This class ensures that sensitive data is:
    - Never exposed in string representation
    - Protected from accidental logging
    - Properly handled in JSON serialization

    Note:
        When used in Pydantic models, this type will automatically handle
        validation and secure storage of sensitive strings.
    """

    @classmethod
    def __get_validators__(cls):
        """Provide validators for Pydantic model integration.

        Returns:
            Generator yielding validation methods used by Pydantic.
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate and convert input to StrongSecret instance.

        Args:
            v: Value to validate and convert.

        Returns:
            StrongSecret instance containing the validated value.

        Note:
            If the input is already a StrongSecret instance, it is returned as-is.
            Otherwise, the input is converted to a new StrongSecret instance.
        """
        if isinstance(v, cls):
            return v
        return cls(v)
