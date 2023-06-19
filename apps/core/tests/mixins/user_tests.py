from django.urls import reverse
from django.utils.http import urlencode
from django.utils.translation import gettext_lazy as _
from rest_framework.test import APIClient

from ...models import User
from ...factories import UserFactory


class UserTestsMixin:

    user = None

    def build_user(self, **kwargs):
        """Builds a new user, without saving it to the DB.

        Returns:
            User: The new user.
        """

        password = kwargs.pop('password', '')

        user = UserFactory.build(**kwargs)

        if password != '':
            user.set_password(password)

        return user

    def create_user(self, **kwargs):
        """Creates a new user.

        Returns:
            User: The new user.
        """

        user_dict = UserFactory.build_dict(**kwargs)
        return User.objects.create_user(**user_dict)

    def create_user_payload(self, **kwargs):
        """Creates valid user payload data.

        Returns:
            dict: The user payload data.
        """

        exclude_fields = kwargs.pop('exclude_fields', [])
        include_fields = kwargs.pop('include_fields', [])

        exclude_fields.extend([f for f in [
            'is_active',
            'is_staff',
            'is_superuser',
        ] if f not in include_fields])

        user_dict = UserFactory.build_dict(include_fields=include_fields,
                                           exclude_fields=exclude_fields,
                                           **kwargs)
        password = user_dict.pop('password', '')

        if password != '' and 'password_1' not in user_dict and 'password_2' not in user_dict:
            user_dict['password_1'] = password
            user_dict['password_2'] = password

        return user_dict


class APITestsMixin(UserTestsMixin):

    api_client = None
    create_view = ''
    destroy_view = ''
    list_view = ''
    partial_update_view = ''
    retrieve_view = ''
    update_view = ''

    def setUp(self):  # pylint: disable=invalid-name
        self.api_client = self.create_api_client()

    def authenticate(self, user, api_client=None, **kwargs):
        """Authenticates an user by force.

        Args:
            user (User): The user to be authenticated.
            api_client (APIClient, optional): The API client to be used.

        Returns:
            User: The authenticated user.
        """

        api_client = self.api_client if not api_client else api_client
        api_client.force_authenticate(user=user)
        return user

    def api_create(self, **kwargs):
        """Sends an API POST request to the create endpoint.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.

        Returns:
            Response: The API response.

        Raises:
            ValueError: If the create view is invalid.
        """

        if not self.create_view:
            error_msg = _('The create view is invalid.')
            raise ValueError(error_msg)

        return self.api_post(self.create_view, **kwargs)

    def api_delete(self, view_name, **kwargs):
        """Sends an API DELETE request.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.
            view_name (str): The view name.

        Returns:
            Response: The API response.
        """

        kwargs['method_name'] = 'delete'
        kwargs['view_name'] = view_name
        return self.api_request(**kwargs)

    def api_destroy(self, **kwargs):
        """Sends an API DELETE request to the destroy endpoint.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.

        Returns:
            Response: The API response.

        Raises:
            ValueError: If the update view is invalid.
        """

        return self.api_delete(self.destroy_view, **kwargs)

    def api_list(self, **kwargs):
        """Sends an API GET request to the list endpoint.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.

        Returns:
            Response: The API response.

        Raises:
            ValueError: If the list view is invalid.
        """

        if not self.list_view:
            error_msg = _('The list view is invalid.')
            raise ValueError(error_msg)

        return self.api_get(self.list_view, **kwargs)

    def api_post(self, view_name, **kwargs):
        """Sends an API POST request.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.
            view_name (str): The view name.

        Returns:
            Response: The API response.
        """

        kwargs['method_name'] = 'post'
        kwargs['view_name'] = view_name
        return self.api_request(**kwargs)

    def api_get(self, view_name, **kwargs):
        """Sends an API GET request.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.
            view_name (str): The view name.

        Returns:
            Response: The API response.
        """

        kwargs['method_name'] = 'get'
        kwargs['view_name'] = view_name
        return self.api_request(**kwargs)

    def api_partial_update(self, **kwargs):
        """Sends an API PATCH request to the partial update endpoint.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.

        Returns:
            Response: The API response.

        Raises:
            ValueError: If the update view is invalid.
        """

        if not self.partial_update_view:
            error_msg = _('The partial update view is invalid.')
            raise ValueError(error_msg)

        return self.api_patch(self.partial_update_view, **kwargs)

    def api_patch(self, view_name, **kwargs):
        """Sends an API PATCH request.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.
            view_name (str): The view name.

        Returns:
            Response: The API response.
        """

        kwargs['method_name'] = 'patch'
        kwargs['view_name'] = view_name
        return self.api_request(**kwargs)

    def api_put(self, view_name, **kwargs):
        """Sends an API PUT request.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.
            view_name (str): The view name.

        Returns:
            Response: The API response.
        """

        kwargs['method_name'] = 'put'
        kwargs['view_name'] = view_name
        return self.api_request(**kwargs)

    def api_request(self, view_name, method_name, **kwargs):
        """Sends an API request.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            method_name (str): The method name.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.
            view_name (str): The view name.

        Returns:
            Response: The API response.
        """

        get_url_kwargs = {
            'urlconf': kwargs.pop('urlconf', None),
            'args': kwargs.pop('url_args', None),
            'kwargs': kwargs.pop('url_kwargs', None),
            'query_params': kwargs.pop('query_params', None),
            'current_app': kwargs.pop('current_app', None),
        }
        url = self.get_url(view_name, **get_url_kwargs)

        api_client = kwargs.pop('api_client', self.api_client)
        data = kwargs.pop('data', None)
        data_format = kwargs.pop('format', 'json')

        method = getattr(api_client, method_name)

        return method(url, data, format=data_format)

    def api_retrieve(self, **kwargs):
        """Sends an API GET request to the retrieve endpoint.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.

        Returns:
            Response: The API response.

        Raises:
            ValueError: If the retrieve view is invalid.
        """

        if not self.retrieve_view:
            error_msg = _('The retrieve view is invalid.')
            raise ValueError(error_msg)

        return self.api_get(self.retrieve_view, **kwargs)

    def api_update(self, **kwargs):
        """Sends an API PUT request to the update endpoint.

        Args:
            api_client (APIClient, optional): The API client to be used.
            current_app (str, optional): The current app name.
            data (dict, optional): The data to be sent.
            format (str, optional): The data format.
            query_params (dict, optional): The query params to included in
                the URL.
            url_args (list, optional): The args to be passed to the URL.
            url_kwargs (dict, optional): The kwargs to be passed to the URL.
            urlconf (str, optional): The URLconf module to use.

        Returns:
            Response: The API response.

        Raises:
            ValueError: If the update view is invalid.
        """

        if not self.update_view:
            error_msg = _('The update view is invalid.')
            raise ValueError(error_msg)

        return self.api_put(self.update_view, **kwargs)

    def create_api_client(self, auth_user=None, **kwargs):
        """Creates and returns an API client.

        Args:
            auth_user (User, optional): The user to authenticate.

        Returns:
            APIClient: The new API client.
        """

        api_client = APIClient()

        if auth_user:
            api_client.force_authenticate(user=auth_user)

        return api_client

    def get_url(self, view_name, urlconf=None, args=None, kwargs=None,
                query_params=None, current_app=None):
        """Gets the complete URL for a view.

        This function is a wrapper for `reverse`, that also includes the
        query params in the URL.

        Args:
            args (list): The args to be passed to the URL.
            current_app (str, optional): The current app name.
            kwargs (dict): The kwargs to be passed to the URL.
            query_params (dict, optional): The query params to included in
                the URL.
            urlconf (str, optional): The URLconf module to use.
            view_name (str): The view name.

        Returns:
            str: The complete URL.
        """

        url = reverse(view_name,
                      urlconf=urlconf,
                      args=args,
                      kwargs=kwargs,
                      current_app=current_app)

        if query_params:
            url += f'?{urlencode(query_params)}'

        return url
