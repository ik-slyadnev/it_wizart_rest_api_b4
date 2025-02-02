import allure

class TestPutV1AccountPassword:
    @allure.title("Проверка смены пароля пользователя")
    def test_put_v1_account_password(self, account_helper, prepare_user):
        """
        Тест смены пароля пользователя через старый пароль

        Шаги:
        1. Регистрация и активация пользователя
        2. Авторизация со старым паролем
        3. Смена пароля
        4. Проверка авторизации с новым паролем
        """
        with allure.step("Регистрируем и активируем нового пользователя"):
            user = account_helper.register_new_user(prepare_user)
        with allure.step(f"Проверяем авторизацию пользователя {user.login} со старым паролем"):
            auth_response = account_helper.auth_client(
                login=user.login,
                password=user.password
            )
            assert auth_response.status_code == 200, "Не удалось авторизоваться со старым паролем"

        with allure.step("Выполняем смену пароля"):
            new_password = "NewPassword123!"
            response = account_helper.change_password(
                password=user.password,
                new_password=new_password
            )
            assert response.status_code == 200, f"Не удалось сменить пароль: {response.text}"

        with allure.step("Проверяем авторизацию с новым паролем"):
            auth_response = account_helper.auth_client(
                login=user.login,
                password=new_password
            )
            assert auth_response.status_code == 200, "Не удалось авторизоваться с новым паролем"
