from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from django.conf import settings


def assign_basic_permissions(user):
    """Assigns the necessary permissions to an `User`.

    This function assigns the necessary permissions to a user, so it can
    change its own data.

    Args:
        user (User): The user to be assigned the permissions.

    Returns:
        User: The user with the assigned permissions.
    """

    from guardian.shortcuts import assign_perm

    assign_perm('core.view_user', user)
    assign_perm('core.change_user', user)

    assign_perm('core.add_email', user)
    assign_perm('core.view_email', user)
    assign_perm('core.change_email', user)
    assign_perm('core.delete_email', user)

    return user


def get_anonymous_user(user_model):
    """Creates an anonymous user. This is necessary for 'django-guardian'.

    See: https://django-guardian.readthedocs.io/en/stable/userguide/custom-user-model.html#custom-user-model-anonymous

    Args:
        user_model (cls): The `User` model.

    Returns:
        User: The created anonymous user.
    """

    return user_model(username=settings.ANONYMOUS_USER_NAME)


def send_email_confirmation(email):
    """Send an email message with a confirmation link to the given email.

    Args:
        email (Email): The email to be confirmed.
    """

    from django.urls import reverse
    from django.utils.http import urlencode

    confirmation_params = {'id': email.id,
                           'confirmation_code': email.confirmation_code}

    confirmation_url = f'https://FRONTEND_URL/CONFIRM_EMAIL_PATH/?{urlencode(confirmation_params)}'

    title_text = _('Just one more step: verify your email address.')

    body_text = _('Use the button below to verify this email address and link it '
                  'to your account. If you prefer, you can also copy and paste '
                  'the link below into your browser. This link will expire in '
                  '24 hours.')

    button_text = _('Verify email address')

    footer_text = _('If you did not create an account with this email address, '
                    'don\'t worry: you can safely ignore this email.')

    html = (  # pylint: disable=superfluous-parens
        f"""
<h1>{title_text}</h1>
<p>{body_text}</p>
<p><a href="{confirmation_url}">{button_text}</a></p>
<p><em>Direct link: {confirmation_url}</em></p>
<p>{footer_text}</p>
        """
    )

    # TODO: Plug the code to send email confirmation here.

    if settings.DEBUG and not settings.TESTING:
        backend_data = {'confirmation_code': str(email.confirmation_code)}
        backend_url = ('https://BACKEND_URL' +
                       reverse('core:email-confirmation', args=[email.pk]))

        print('\n', '='*80, sep='')
        print('\nEMAIL CONFIRMATION DATA:\n')
        print(f'Email: {email.address}')
        print(f'Confirmation Code: {email.confirmation_code}')
        print(f'Backend URL: {backend_url=}')
        print(f'Backend Payload Data: {backend_data=}\n')
        print('-'*80)
        print('\nEMAIL CONFIRMATION HTML:')
        print(html)
        print('='*80)


def user_authentication_rule(user):
    """User authentication rule for Simple JWT.

    Args:
        user (User): The user to be authenticated.

    Returns:
        bool: Whether the user can be considered authenticated or not.

    Raises:
        AuthenticationFailed: If the user email is not confirmed.
    """

    if not user.primary_email.is_confirmed:
        error_msg = _('Email is not confirmed.')
        raise exceptions.AuthenticationFailed({'email': error_msg})

    return user is not None and user.is_active
