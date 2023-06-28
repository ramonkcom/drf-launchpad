🔙 [Back to documentation](./index.md)

---

# Project structure

The project is structured in a way that makes it easy to extend and maintain. The project is divided in three main folders: `config`, `apps` and `utils`. The `notebooks` folder is just a place to put Jupyter notebooks for testing and experimenting (more on [the `notebooks` directory section](#the-notebooks-directory)) and the `docs` folder is where this documentation lives.

```
drf-lauchpad
├── apps
├── config
├── docs
├── notebooks
└── utils
```

The `config` directory is the Django project directory. It is a little bit different from the default Django project structure because the settings are split to make them easier to maintain. You can read more about it in the [`config` directory ](#the-config-directory).

The `apps` directory is where the Django apps live. It is meant to keep apps isolated from configuration files. The `core` directory inside it is the directory of the main app, where all the user related functionality resides. You can read more about it in the [`app` directory](#the-core-app) section.

The `utils` directory holds all the utilities and helpers that are used across the project. You can read more about its contents in the [`utils` directory](#the-utils-directory) section.

- [The `config` directory](#the-config-directory)
- [The `apps` directory](#the-apps-directory)
- [The `utils` directory](#the-utils-directory)
- [The `notebooks` directory](#the-notebooks-directory)

---

## The `config` directory

The `config` directory is the Django project directory. But different from the default Django project structure, the `settings.py` file here is a module split in multiple files. This is to make it easier to maintain the settings, as `settings.py` tend to get humongous as the project grows.

```
config
├── asgi.py
├── settings
│   ├── __init__.py
│   ├── common.py
│   ├── django_apps.py
│   ├── django_auth.py
│   ├── django_db.py
│   ├── django_email.py
│   ├── django_general.py
│   ├── django_i18n.py
│   ├── django_middleware.py
│   ├── django_static.py
│   ├── django_templates.py
│   ├── drf_spectacular.py
│   ├── guardian.py
│   ├── rest_framework.py
│   └── rest_framework_simplejwt.py
├── static
│   └── css
│       └── custom.css
├── urls.py
└── wsgi.py
```

The upside of this approach is that you can easily find the settings you want to change and avoid things messing up, as they are grouped by functionality or by package. For instance, the entire content of `settings/guardian.py` is as follows:

```python
"""
DJANGO GUARDIAN SETTINGS

About Django Guardian:
- https://django-guardian.readthedocs.io/en/stable/

Full list of Django Guardian settings:
- https://django-guardian.readthedocs.io/en/stable/configuration.html#optional-settings
"""

ANONYMOUS_USER_NAME = 'anonymous'
GUARDIAN_GET_INIT_ANONYMOUS_USER = 'utils.permissions.get_anonymous_user'
```

Notice that the files also contain useful comments and links to the documentation of the package or Django functionality to which they are related, which is nice.

The small downside of this approach is that every time you install a new package that requires settings, you have to create a new file for it and link it in `__init__.py`, like this:

```python
# NOTE: This is the `settings/__init__.py`
# You have to create settings files and import them here
# everytime you install a new package.

# DJANGO SETTINGS
from .django_general import *
from .django_apps import *
from .django_templates import *
from .django_middleware import *
from .django_db import *
from .django_auth import *
from .django_static import *
from .django_email import *
from .django_i18n import *

# THIRD-PARTY SETTINGS
from .drf_spectacular import *
from .guardian import *
from .rest_framework import *
from .rest_framework_simplejwt import *
# ex: from .[PACKAGE_SETTINGS_FILE] import *
```

---

## The `apps` directory

The `apps` directory is where the Django apps live. It is meant to keep apps isolated from configuration files. Your apps should be created inside this directory, along with the `core` app, which is the main app of the project:

```
apps
   └── core
       ├── admin
       ├── apps.py
       ├── factories
       ├── managers
       ├── migrations
       ├── models
       ├── serializers
       ├── signals
       ├── static
       ├── tests
       ├── urls.py
       └── views
    └── your_new_app_1
    └── your_new_app_2
    └── your_new_app_3
```

### About the structure of the `core` app

Normally all the models reside in a single file named `models.py`. The same applies to serializers, views etc. However, as the project grows, these files tend to get hard to maintain. So, in this project, these files are split in multiple files, making things more organized. For instance, the `models` directory contains the following files:

```
models
├── __init__.py
├── email.py
├── profile.py
└── user.py
```

Whereas `models/__init__.py` looks like this:

```python
from .user import User
from .profile import Profile
from .email import Email
```

Following the same logic, the `serializers` directory contains the following files:

```
serializers
├── __init__.py
├── email.py
├── profile.py
└── user.py
```

Whereas `serializers/__init__.py` looks like this:

```python
from .user import UserSerializer
from .profile import ProfileSerializer
from .email import EmailSerializer
```

And so on. This way, it is easier to find the code you want to change and avoid modifying things unintentionally.

---

## The `utils` directory

The `utils` directory holds all the utilities and helpers that are used across the project. These might be functions, classes, mixins, decorators etc, and currently it is organized as follows:

```
utils
├── auth.py
├── factories
│   └── mixins
│       └── dict.py
├── helpers.py
├── mail.py
├── permissions.py
└── tests
    └── mixins
        └── api.py
```

I encourage you to read the code in these files to understand what they do and how they work. They are pretty simple and straightforward. But, basically:

- `auth.py` contains the `user_authentication_rule` function [used by Simple JWT during the authentication](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#user-authentication-rule). Any custom authentication logic or related code that may come up in the future can be placed here.
- `factories/mixins` contains a mixin that allows you to create a dictionary from a factory object, which is useful for testing. Any mixins intended for factories that may come up in the future can be placed here.
- `helpers.py` contains helpful functions to handle models. Any function that may come up in the future that don't fit in any other file can be placed here.
- `mail.py` contains classes and functions to help templating and sending emails.
- `permissions.py` contains functions related to permissions such as the `get_anonymous_user` function [used by Django Guardian](https://django-guardian.readthedocs.io/en/stable/configuration.html#anonymous-user-name) and `assign_initial_permissions` that is called by a signal to assign basic permissions to a new user. Any custom permission logic or related code that may come up in the future can be placed here.
- `tests/mixins` contains mixins with common funcionalities for testing. Any mixins intended for testing that may come up in the future can be placed here.

---

## The `notebooks` directory

The `notebooks` directory is just a place to store [Jupyter](https://jupyterlab.readthedocs.io/en/stable/) notebooks, and it is not necessary for the project to function. The only Jupyter notebook included in this directory is `django.ipynb`, which contains the necessary code to load the Django environment in a notebook.

I only included this directory in the project because in my personal experience Jupyter notebooks have proven to be very useful for testing and experimenting the code, and I almost always use them in my projects. <ins>However, if you don't want to use Jupyter notebooks, you can safely delete this directory.</ins>

As Jupyter has a lot of dependencies, it is **<ins>not included</ins>** in the `requirements.txt`. So if you do want to use it, you have to install it manually by running:

```bash
pip install jupyter
```

---

🔙 [Back to documentation](./index.md)
