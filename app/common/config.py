from dataclasses import dataclass, field
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    """
    기본 Configuration
    """
    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DEBUG: bool = False
    TEST_MODE: bool = False
    DEV_MODE: bool = False
    DB_HOST: str = 'localhost'
    REDIS_HOST: str = 'localhost'
    TRUSTED_HOSTS: list = field(default_factory=lambda: ["*"])
    ALLOW_SITE: list = field(default_factory=lambda: ["*"])


@dataclass
class LocalConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class ProdConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DB_ECHO: bool = False


@dataclass
class StageConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DB_ECHO: bool = False


@dataclass
class DevConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEV_MODE: bool = True
    DB_ECHO: bool = False


@dataclass
class TestConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


def conf():
    """
    환경 불러오기
    :return:
    """
    config = dict(prod=ProdConfig, stage=StageConfig, local=LocalConfig, test=TestConfig, dev=DevConfig)
    return config[environ.get("API_ENV", "local")]()


