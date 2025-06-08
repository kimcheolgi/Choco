from dataclasses import asdict
from os import environ
from app.common.config import conf
from dotenv import load_dotenv
load_dotenv()
env = environ.get("API_ENV", "local")
c = conf()
conf_dict = asdict(c)
EXCEPT_PATH_LIST = ["/", "/openapi.json", "/api/v1/common-util/health"]
EXCEPT_PATH_REGEX = "^(/docs|/redoc|/api/auth)"

MYSQL_HOST = environ.get('MYSQL_HOST')
MYSQL_PORT = environ.get('MYSQL_PORT')
MYSQL_DATABASE = environ.get('MYSQL_DATABASE')
MYSQL_USER = environ.get('MYSQL_USER')
MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD')
