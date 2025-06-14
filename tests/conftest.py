import os

from .mocks import *  # NOQA (including mock test fixtures)

os.environ['TESTING'] = 'pytest'

from libutil import engines, util


def setup_engine_env(*engine_names):
    assert util.IS_DEV

    for engine_name in engine_names:
        with engines.get_engine('test').connect() as conn:
            conn.execute(f'DROP DATABASE IF EXISTS {engine_name}')
            conn.execute(f'CREATE DATABASE {engine_name}')


setup_engine_env('todolist')
