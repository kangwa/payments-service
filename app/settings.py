from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTAuthSettings(BaseSettings):
    secret_key: str = "some-secret-key"
    algorithm: str = "HS256"


class Settings(BaseSettings):
    app_name: str = "Payments API"
    debug: bool = False
    jwt: JWTAuthSettings
    db_url: str = "sqlite:///test.db"
    db_pool_size: int = 1
    db_max_overflow: int = 1
    db_pool_recycle: int = 1
    db_echo: int = 1
    db_connect_args: dict = {
        "check_same_thread": False
    }  # SQLite-specific connection arguments for thread safety
    admin_user_model: str
    admin_user_model_username_field: str
    admin_secret_key: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings(jwt=JWTAuthSettings())
