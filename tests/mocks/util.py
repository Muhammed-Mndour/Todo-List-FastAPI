from unittest import mock

import pytest

from libutil import util


def register_mock(mock_path):
    def wrapped(mock_callable):
        def mock_fixture():
            with mock.patch(mock_path, new_callable=mock_callable) as mock_obj:
                yield mock_obj

        if util.IS_TESTING:
            return pytest.fixture(scope='session', autouse=True)(mock_fixture)
        elif util.IS_STAGING or util.IS_DEV:
            return mock_callable
        else:
            raise Exception('Mocking is only supported in testing, staging, or dev environments')

    return wrapped


def register_mock_function(mock_path):
    def wrapped(mock_callable):
        def mock_fixture():
            with mock.patch(mock_path, new=mock_callable) as mock_obj:
                yield mock_obj

        if util.IS_TESTING:
            return pytest.fixture(scope='session', autouse=True)(mock_fixture)
        elif util.IS_STAGING or util.IS_DEV:
            return mock_callable
        else:
            raise Exception('Mocking is only supported in testing, staging, or dev environments')

    return wrapped
