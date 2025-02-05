from hamcrest import assert_that, has_properties


class PostV1AccountResponseChecker:
    """Класс для проверки ответа метода POST v1/account"""

    @staticmethod
    def check_response(actual_user, expected_user):
        """
        Проверяет соответствие свойств фактического пользователя ожидаемым значениям

        Args:
            actual_user: Фактический пользователь, полученный после регистрации
            expected_user: Ожидаемый пользователь с эталонными данными
        """
        assert_that(actual_user, has_properties({
            'login': expected_user.login,
            'email': expected_user.email,
            'password': expected_user.password
        }))
