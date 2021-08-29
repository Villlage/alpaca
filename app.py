from typing import Type, Optional
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy import MetaData
from flask_login import LoginManager
import logging
from config import Config, LocalConfig, TestingConfig, StagingConfig, ProductionConfig


DEVELOPMENT = "development"
TESTING = "testing"
STAGING = "staging"
PRODUCTION = "production"


app = Flask(
    __name__, static_folder="./client/dist", template_folder="./client/build"
)  # type: Flask

config_map = {
    DEVELOPMENT: LocalConfig,
    TESTING: TestingConfig,
    STAGING: StagingConfig,
    PRODUCTION: ProductionConfig,
}

config = config_map[app.env]  # type: ignore
app.config.from_object(config)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def _get_logger(log_level: str) -> logging.Logger:
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    return logger


def get_env() -> Optional[str]:
    return app.env


metadata = MetaData(naming_convention=convention)  # # type: MetaData
db = SQLAlchemy(app, metadata=metadata)  # type: SQLAlchemy
login_manager = LoginManager()  # type: LoginManager
login_manager.init_app(app)
migrate = Migrate(app, db)  # type: Migrate
ma = Marshmallow(app)  # type: Marshmallow
logger = _get_logger(config.LOG_LEVEL)  # type: logging.Logger


# Models
from models.user import User
from models.plaid_item import PlaidItem
from models.plaid_account import PlaidAccount

# Routes
import controller.user_routes
import controller.react_routes
import controller.plaid_routes
