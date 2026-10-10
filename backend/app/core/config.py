import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    mysql_host: str
    mysql_port: int
    mysql_database: str
    mysql_user: str
    mysql_password: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30
    refresh_token_days: int = 7

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
        )


def _load() -> Settings:
    secret = os.environ["JWT_SECRET"]  # falla al arrancar si no esta definido
    if len(secret) < 32:
        raise RuntimeError("JWT_SECRET debe tener al menos 32 caracteres")
    return Settings(
        mysql_host=os.environ["MYSQL_HOST"],
        mysql_port=int(os.environ["MYSQL_PORT"]),
        mysql_database=os.environ["MYSQL_DATABASE"],
        mysql_user=os.environ["MYSQL_USER"],
        mysql_password=os.environ["MYSQL_PASSWORD"],
        jwt_secret=secret,
        access_token_minutes=int(os.environ.get("ACCESS_TOKEN_MINUTES", 30)),
        refresh_token_days=int(os.environ.get("REFRESH_TOKEN_DAYS", 7)),
    )


settings = _load()
