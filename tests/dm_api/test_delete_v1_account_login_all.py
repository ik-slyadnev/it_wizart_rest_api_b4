import pytest
import allure
from requests.exceptions import HTTPError


class TestDeleteV1AccountLoginAll:

    @allure.title("Проверка выхода из системы на всех устройствах")
    def test_delete_v1_account_login_all(self, auth_user, login_helper):
        """
        Тест выхода из аккаунта на всех устройствах с использованием авторизованного пользователя

        Шаги:
        1. Используем авторизованного пользователя (из фикстуры auth_user)
        2. Выполняем выход из системы на всех устройствах через login_helper
        3. Проверяем успешность выхода
        """
        with allure.step("Выполняем выход из системы на всех устройствах"):
            response = login_helper.logout_all()
            assert response.status_code == 204, "Неверный код ответа при выходе из системы на всех устройствах"

        with allure.step("Проверяем что пользователь не авторизован"):
            with pytest.raises(HTTPError) as exc_info:
                auth_user.helper.get_current_user()

            assert exc_info.value.response.status_code == 401, "Пользователь все еще авторизован после выхода"
