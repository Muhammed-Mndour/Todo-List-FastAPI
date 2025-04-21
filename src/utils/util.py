import os

import pydantic
from humps import camelize

IS_PRODUCTION = os.getenv('ENV') == 'production'
IS_STAGING = os.getenv('ENV') == 'staging'
IS_DEV = os.getenv('ENV') == 'dev'
IS_TESTING = os.getenv('TESTING') == 'pytest'


class BaseModel(pydantic.BaseModel):
    class Config:
        use_enum_values = True
        populate_by_name = True
        alias_generator = camelize
