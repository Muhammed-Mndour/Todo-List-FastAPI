import sqlalchemy

from utils import util

ENGINES = {}


def get_engine(name):
    if name not in ENGINES:
        raise Exception('Engine does not exist')
    return ENGINES[name]


def create_engine(name, url, **create_engine_kwargs):
    if name in ENGINES:
        raise Exception('Engine already exists')

    default_kwargs = {
        'pool_pre_ping': True,
        'pool_size': 5,
        'max_overflow': 10,
        'pool_recycle': 600,
    }

    create_engine_kwargs.update(default_kwargs)

    engine = sqlalchemy.create_engine(url, **create_engine_kwargs)

    ENGINES[name] = engine


def define_engines():
    pass


def define_engines_dev():
    create_engine('test', 'mysql+mysqldb://root:root@mysqldb:3306/')
    create_engine('todolist', 'mysql+mysqldb://root:root@mysqldb:3306/todolist')


if util.IS_DEV:
    define_engines_dev()
else:
    define_engines()
