import os
from dataclasses import dataclass
from urllib.parse import quote_plus


@dataclass(frozen=True)
class Settings:
    mysql_host: str
    mysql_port: int
    mysql_database: str
    mysql_user: str
    mysql_password: str
    jwt_secret: str
    mongo_url: str = "mongodb://localhost:27017/?authSource=admin"
    mongo_db: str = "medreminder_logs"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30
    refresh_token_days: int = 7

    @property
    def database_url(self) -> str:
        user_enc = quote_plus(self.mysql_user)
        pass_enc = quote_plus(self.mysql_password)
        return (
            f"mysql+pymysql://{user_enc}:{pass_enc}"
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
        mongo_url=os.environ.get("MONGO_URL", "mongodb://localhost:27017/?authSource=admin"),
        mongo_db=os.environ.get("MONGO_DB", "medreminder_logs"),
        access_token_minutes=int(os.environ.get("ACCESS_TOKEN_MINUTES", 30)),
        refresh_token_days=int(os.environ.get("REFRESH_TOKEN_DAYS", 7)),
    )


settings = _load()
