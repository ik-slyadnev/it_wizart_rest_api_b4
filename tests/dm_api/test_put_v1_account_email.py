import pytest
import allure
from requests.exceptions import HTTPError

class TestPutV1AccountEmail:
    @allure.title("Проверка смены email пользователя")
    def test_put_v1_account_email(self, account_helper, dm_api_facade, mailhog_facade, login_helper, prepare_user):
        """
        Тест на смену email пользователя

        Шаги:
        1. Регистрация и активация пользователя
        2. Логин в систему
        3. Смена email
        4. Проверка невозможности входа до подтверждения
        5. Получение и активация токена подтверждения
        6. Проверка возможности входа после подтверждения
        """
        with allure.step("Регистрируем нового пользователя"):
            user = account_helper.register_new_user(prepare_user)

        with allure.step(f"Выполняем вход пользователем {user.login}"):
            response = login_helper.login(user.login, user.password)
            assert response.status_code == 200

        with allure.step("Отправляем запрос на смену email"):
            new_email = f"new_{user.login}@example.com"
            response = dm_api_facade.account_api.put_v1_account_email(
                login=user.login,
                password=user.password,
                new_email=new_email
            )
            assert response.status_code == 200

        with allure.step("Проверяем невозможность входа до подтверждения нового email"):
            with pytest.raises(HTTPError) as exc_info:
                login_helper.login(user.login, user.password)
            assert exc_info.value.response.status_code == 403

        with allure.step("Получаем и активируем токен подтверждения email"):
            email_change_token = account_helper.get_registration_token(user.login)
            account_helper.activate_account(email_change_token)

        with allure.step("Проверяем возможность входа после подтверждения email"):
            response = login_helper.login(user.login, user.password)
            assert response.status_code == 200
