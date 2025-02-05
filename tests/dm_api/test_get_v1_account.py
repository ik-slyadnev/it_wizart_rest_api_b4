from hamcrest import assert_that, equal_to
from common.http_checkers import check_status_code
from common.checkers.checker_get_v1_account import GetV1AccountResponseChecker

class TestGetV1Account:

    def test_get_v1_account_auth(self, auth_user):
        """
        Тест на получение информации об авторизованном пользователе

        Шаги:
        1. Получаем информацию об авторизованном пользователе
        2. Проверяем ответ
        """
        # with check_status_code(200, "User must be authenticated"):
        response = auth_user.helper.get_current_user()
        GetV1AccountResponseChecker.check_response(response, auth_user.user)

    def test_get_v1_account_no_auth(self, dm_api_facade):
        """
        Тест на получение информации без авторизации

        Шаги:
        1. Пытаемся получить информацию о пользователе без авторизации
        2. Проверяем что получаем ошибку авторизации (401)
        """
        with check_status_code(401, "User must be authenticated"):
            response = dm_api_facade.account_api.get_v1_account()

