import os
import pytest

from mock import patch

from servant.config import Config


@pytest.fixture
def config():
    return Config()

class DummyConfig(object):
    DB_NAME = 'foo'
    DB_HOST = 'baz.bar'
    AGE = 42
    SOMETHING = {'one': 1, 'two': 2}

def test_config_from_obj(config):
    config.from_object(DummyConfig)
    assert config.DB_NAME == 'foo'
    assert config.DB_HOST == 'baz.bar'
    assert config.AGE == 42
    assert config.SOMETHING == {'one': 1, 'two': 2}


def _assert_config_values(config):
    assert config.DUMMY_CONFIG == True
    assert config.VERSION == 1.0
    assert config.CALCULATOR_NAME == 'calculator_service'
    with pytest.raises(AttributeError):
        assert config.DOESNT_EXIST

def test_config_from_module(config):
    assert config.from_module('calculator_service.config')
    _assert_config_values(config)

def test_config_from_bad_module(config):
    with pytest.raises(ImportError) as e:
        config.from_module('foobar')
    assert 'Unable to load configuration file (No module named foobar)' in str(e)

@patch.dict(os.environ, {'CALC_SERVICE_CONFIG': 'calculator_service.config'})
def test_config_from_env_var(config):
    assert config.from_envvar('CALC_SERVICE_CONFIG')
    _assert_config_values(config)

def test_config_from_bad_env_var(config):
    with pytest.raises(RuntimeError) as e:
        config.from_envvar('CALC_SERVICE_CONFIG')
    assert "The environment variable 'CALC_SERVICE_CONFIG' is not set" in str(e)
