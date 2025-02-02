import allure

class TestPostV1AccountLogin:
    @allure.title("Проверка успешной авторизации пользователя")
    def test_post_v1_account_login(self, account_helper, login_helper, prepare_user):
        with allure.step("Регистрируем и активируем нового пользователя"):
            user = account_helper.register_new_user(prepare_user)

        with allure.step(f"Выполняем авторизацию пользователя {user.login}"):
            response = login_helper.login(
                login=user.login,
                password=user.password
            )
            assert response.status_code == 200, "Не удалось авторизоваться"
