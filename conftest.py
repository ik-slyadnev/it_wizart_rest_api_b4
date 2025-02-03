import pytest
import yaml
import os
from vyper import v
from faker import Faker
from collections import namedtuple
from common.logger import setup_logging
from configs.configuration import Configuration
from services.dm_api.dm_api_facade import DMApiAccount
from services.mailhog.mailhog_facade import MailHogAPI
from helpers.account_helper import AccountHelper
from helpers.login_helper import LoginHelper

################################################################################
# Инициализация базовых компонентов
################################################################################

# Инициализация логгера при старте тестов
setup_logging()

# Инициализация генератора тестовых данных
fake = Faker()


################################################################################
# Функции для работы с конфигурацией
################################################################################

def load_config(config_file):
    """
    Загружает конфигурацию из yaml файла
    Args:
        config_file: путь к файлу конфигурации
    Returns:
        dict: загруженная конфигурация
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Конфигурационный файл {config_file} не найден")

    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


def pytest_addoption(parser):
    """Добавляет опцию для указания окружения при запуске тестов"""
    parser.addoption('--env', action='store', default='dev',
                     help='Окружение для запуска тестов (dev, stage)')


################################################################################
# Фикстуры конфигурации
################################################################################

@pytest.fixture(scope='session')
def config(request):
    """
    Инициализация конфигурации с помощью vyper
    """
    env = request.config.getoption('--env')

    # Настройка vyper
    v.set_config_name(env)  # имя файла без расширения
    v.add_config_path(os.path.join(os.path.dirname(__file__), 'configs'))  # путь к папке с конфигами
    v.set_config_type('yaml')  # тип конфига

    try:
        v.read_in_config()
    except Exception as e:
        raise Exception(f"Error reading config file: {e}")

    return v


@pytest.fixture
def main_config(config):
    """Конфигурация для DM API"""
    return Configuration(
        host=config.get_string('service.dm_api.host'),
        headers={'Content-Type': 'application/json'},
        disable_log=config.get_bool('service.dm_api.disable_log')
    )

@pytest.fixture
def mailhog_config(config):
    """Конфигурация для Mailhog"""
    return Configuration(
        host=config.get_string('service.mailhog.host'),
        disable_log=config.get_bool('service.mailhog.disable_log')
    )

################################################################################
# Фикстуры для работы с пользователями
################################################################################

@pytest.fixture
def prepare_user():
    """
    Фикстура для генерации тестового пользователя
    Returns:
        namedtuple: User с полями login, password, email
    """
    login = fake.user_name()
    password = fake.password()
    email = f"{login}@{fake.free_email_domain()}"

    User = namedtuple("User", ["login", "password", "email"])
    return User(login=login, password=password, email=email)


@pytest.fixture
def auth_user(account_helper, prepare_user):
    """
    Фикстура для создания и авторизации пользователя
    Args:
        account_helper: хелпер для работы с аккаунтом
        prepare_user: фикстура с данными пользователя
    Returns:
        namedtuple: AuthUserData с полями user и helper
    """
    user = account_helper.register_new_user(user=prepare_user)
    auth_response = account_helper.auth_client(
        login=user.login,
        password=user.password
    )
    assert auth_response.status_code == 200, "Ошибка авторизации пользователя"

    AuthUserData = namedtuple('AuthUserData', ['user', 'helper'])
    return AuthUserData(user=user, helper=account_helper)


################################################################################
# Фикстуры фасадов для работы с API
################################################################################

@pytest.fixture
def dm_api_facade(main_config):
    """
    Фасад для работы с DM API
    Returns:
        DMApiAccount: объект для взаимодействия с API аккаунта
    """
    return DMApiAccount(configuration=main_config)


@pytest.fixture
def mailhog_facade(mailhog_config):
    """
    Фасад для работы с Mailhog
    Returns:
        MailHogAPI: объект для взаимодействия с API почтового сервиса
    """
    return MailHogAPI(configuration=mailhog_config)


################################################################################
# Фикстуры хелперов
################################################################################

@pytest.fixture
def account_helper(dm_api_facade, mailhog_facade):
    """
    Хелпер для работы с аккаунтом
    Args:
        dm_api_facade: фасад DM API
        mailhog_facade: фасад Mailhog
    Returns:
        AccountHelper: объект с методами для работы с аккаунтом
    """
    return AccountHelper(dm_api_facade, mailhog_facade)


@pytest.fixture
def login_helper(dm_api_facade):
    """
    Хелпер для работы с логином
    Args:
        dm_api_facade: фасад DM API
    Returns:
        LoginHelper: объект с методами для работы с логином
    """
    return LoginHelper(dm_api_facade)
