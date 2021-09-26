import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    DEBUG = False
    TESTING = False
    LOG_LEVEL = "INFO"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "thisisasecretkey")

    PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID", "5ae9039e900e950013499ad4")
    PLAID_SECRET = os.getenv("PLAID_SECRET", "b9b6191d2b3e6b4d958e70f7c80a94")
    PLAID_PUBLIC_KEY = os.getenv("PLAID_PUBLIC_KEY", "a004a070f0629da694fbae916414f3")
    PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "PKFI72LSSACG5790KTRZ")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "LqKs5XK32j9BrGcv4yJHI0pNxZTe3dr5qam590Er")
    ALPCA_API_BASE_URL = os.getenv("ALPCA_API_BASE_URL", "https://paper-api.alpaca.markets")
    TELEGRAM_KEY = os.getenv("TELEGRAM_KEY", "2020412177:AAF5gHMeZCoisqcsLJKeJ44Yh9_5QCS2tUo")

class LocalConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = "postgres://localhost/alpaca"


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://localhost/alpaca_test"
    )
    TELEGRAM_KEY = os.getenv("TELEGRAM_KEY", "Nope")


class StagingConfig(Config):
    LOG_LEVEL = "INFO"


class ProductionConfig(Config):
    LOG_LEVEL = "INFO"
