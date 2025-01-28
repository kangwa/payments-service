from passlib.context import CryptContext

from app.core.auth.interfaces.password_hasher_interface import PasswordHasher


class BCryptPasswordHasher(PasswordHasher):
    """Password hasher implementation using the Argon2 hashing algorithm.

    This class implements the PasswordHasher interface using the Passlib library
    with Argon2 as the primary hashing scheme. Argon2 is the winner of the
    Password Hashing Competition and provides strong security against various
    attack vectors including GPU/FPGA attacks.

    Note:
        Despite the class name referencing BCrypt, this implementation actually uses
        Argon2. The class name should be updated to ArgonPasswordHasher for clarity.

    Attributes:
        pwd_context (CryptContext): Passlib context configured for Argon2 hashing.
    """

    def __init__(self):
        """Initialize the password hasher with Argon2 configuration.

        The hasher is configured to use Argon2 as the primary scheme with automatic
        deprecation handling for backwards compatibility.
        """
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: The plain text password to verify.
            hashed_password: The previously hashed password to compare against.

        Returns:
            True if the password matches the hash, False otherwise.

        Note:
            This method is timing-attack safe as it uses constant-time comparison.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash(self, password: str) -> str:
        """Hash a password using Argon2.

        Args:
            password: The plain text password to hash.

        Returns:
            A secure hash of the password, including algorithm information
            and salt in the standard PHC string format.

        Note:
            The resulting hash string includes the algorithm parameters,
            salt, and version information for future verification.
        """
        return self.pwd_context.hash(password)
