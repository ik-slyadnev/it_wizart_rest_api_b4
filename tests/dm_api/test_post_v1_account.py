import pytest
from common.http_checkers import check_status_code
from common.checkers.checker_post_v1_account import PostV1AccountResponseChecker

class TestPostV1Account:
    def test_post_v1_account(self, account_helper, prepare_user):
        """
        Тест проверяет успешную регистрацию нового пользователя
        """
        user = account_helper.register_new_user(prepare_user)
        PostV1AccountResponseChecker.check_response(user, prepare_user)


    @pytest.mark.parametrize('login, email, password', [
        ('a', 'test@test.com', 'test123'),
        ('test_user', 'invalid_email', 'test123'),
        ('test_user', 'test@test.com', '12345')
    ])
    def test_post_v1_account_invalid_data(self, dm_api_facade, login, email, password):
        """Тест проверяет ответ сервера при попытке регистрации с невалидными данными"""
        with check_status_code(expected_status_code=400, expected_message="Validation failed"):
            dm_api_facade.account_api.post_v1_account(login=login, email=email, password=password)
