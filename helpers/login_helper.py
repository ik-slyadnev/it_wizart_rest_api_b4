from requests import Response
import allure

class LoginHelper:
    def __init__(self, dm_api_facade):
        self.dm_api_facade = dm_api_facade

    @allure.step("Авторизация пользователя")
    def login(self, login: str, password: str) -> Response:
        """
        Авторизация пользователя

        :param login: Логин пользователя
        :param password: Пароль пользователя
        :return: Response объект с результатом авторизации
        """
        response = self.dm_api_facade.login_api.post_v1_account_login(
            login=login,
            password=password
        )
        return response

    @allure.step("Очистка токенов авторизации")
    def _clear_auth_tokens(self):
        """
        Очистка токенов авторизации
        """
        for api in [self.dm_api_facade.account_api, self.dm_api_facade.login_api]:
            api.session.headers.pop("X-Dm-Auth-Token", None)

    @allure.step("Выход из системы")
    def logout(self) -> Response:
        """
        Выход из системы (удаление текущей сессии)

        :return: Response объект с результатом выхода из системы
        """
        response = self.dm_api_facade.login_api.delete_v1_account_login()
        if response.status_code == 204:
            self._clear_auth_tokens()
        return response

    @allure.step("Выход из системы на всех устройствах")
    def logout_all(self) -> Response:
        """
        Выход из системы на всех устройствах

        :return: Response объект с результатом выхода из системы на всех устройствах
        """
        response = self.dm_api_facade.login_api.delete_v1_account_login_all()
        if response.status_code == 204:
            self._clear_auth_tokens()
        return response
