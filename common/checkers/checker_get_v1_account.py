from hamcrest import assert_that, equal_to, has_entries, has_items


class GetV1AccountResponseChecker:
    """Класс для проверки ответа метода GET v1/account"""

    @staticmethod
    def check_response(response, expected_user):
        """
        Проверяет ответ GET v1/account для авторизованного пользователя

        Args:
            response: Ответ от API
            expected_user: Ожидаемый пользователь с эталонными данными
        """
        assert_that(response.status_code, equal_to(200))

        resource = response.json()['resource']
        assert_that(resource, has_entries({
            'login': expected_user.login,
            'roles': has_items('Guest', 'Player'),
            'rating': has_entries({
                'enabled': True,
                'quality': 0,
                'quantity': 0
            }),
            'settings': has_entries({
                'colorSchema': 'Modern',
                'paging': has_entries({
                    'postsPerPage': 10,
                    'commentsPerPage': 10,
                    'topicsPerPage': 10,
                    'messagesPerPage': 10,
                    'entitiesPerPage': 10
                })
            })
        }))
