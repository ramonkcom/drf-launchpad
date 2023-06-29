# DRF Lauchpad

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/Rest%20Framework-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/Guardian-109989?style=for-the-badge&logo=django&logoColor=005949)
![image](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

---

_**⚠️ IMPORTANT:** This project is still under development. It is not ready for production yet, as it might introduce breaking changes abruptly. Use it at your own risk._

---

DRF Lauchpad is a boilerplate for **quickly starting new RESTful API projects using Django and Django Rest Framework (DRF)**. It provides all the basic code and structure for developing RESTful API with Django and DRF, such as:

**🥸 <ins>Easy to customize and extend user model that:</ins>**

- Uses email as username
- Supports multiple emails
- Keeps personal data in a separate model
- Object level permissions
- Has all signals in place

---

**🔌 <ins>Easy to customize and extend API endpoints for user management, including:</ins>**

- Signup endpoint that requires email confirmation¹
- Endpoint for asking new confirmation email¹
- Endpoint for confirming email
- Endpoint to add new email addresses¹
- Endpoint to set a email address as primary (for login)
- Endpoint to remove email addresses
- Endpoint to update user data
- Endpoint for asking password recovery¹
- Endpoint for safely resetting password

_¹ These endpoints will send emails to the user, so you have to **configure the email service** of your choice to make them work. You can find the [instructions here](./docs/email-sending.md)._

---

**🔒 <ins>API for JWT authentication, with:</ins>**

- Login endpoint
- Token renewal endpoint
- Token verification endpoint

---

**🍒 <ins>Nice extra features, such as:</ins>**

- Swagger documentation with [DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/) already configured
- [Django Guardian](https://django-guardian.readthedocs.io/en/stable/) already configured for object level permissions
- Factories for all models using [Factory Boy](https://factoryboy.readthedocs.io/en/stable/) to make testing easier
- Test cases set up for all models, managers and endpoints
- Admin customized for the custom user model, supporting multiple emails and personal data
- Settings split, organized and documented in multiple files for easier maintenance

---

## Roadmap:

The following features are planned for the next releases:

- [x] Use Django native email functionality in the architecture
- [ ] Include Brazilian Portuguese translations
- [ ] Add authentication via Google, Facebook, Twitter and Github
- [ ] Rewrite the documentation using [MkDocs](https://www.mkdocs.org/) or [Sphinx](https://www.sphinx-doc.org/)

---

## Documentation:

Most of the things in the project are obvious, but I highly recommend that you read the documentation to better understand the project structure and how things were designed to work.

Of course, you don't need to read all the sections from top to bottom. They are meant to be as independent from each other as possible so you can consult the sections as you go, according to your needs.

- [Quick start](./docs/index.md#quick-start)
- [Project structure](./docs/project-structure.md)
  - [The `config` directory](./docs/project-structure.md#the-config-directory)
  - [The `apps` directory](./docs/project-structure.md#the-apps-directory)
  - [The `utils` directory](./docs/project-structure.md#the-utils-directory)
  - [The `notebooks` directory](./docs/project-structure.md#the-notebooks-directory)
- [Custom user model](./docs/custom-user-model.md)
  - [The `User`, `Profile` and `Email` models](./docs/custom-user-model.md#the-user-profile-and-email-models)
  - [The `core.signals`](./docs/custom-user-model.md#the-coresignals)
  - [The `UserSerializer`](./docs/custom-user-model.md#the-userserializer)
  - [The `UserFactory`](./docs/custom-user-model.md#the-userfactory)
- [Permissions](./docs/permissions.md)
- [Email sending](./docs/email-sending.md)
  - [Configuring Django mail system](./docs/email-sending.md#configuring-django-mail-system)
  - [Customizing the email content](./docs/email-sending.md#customizing-the-email-content)
  - [Customizing the sending method](./docs/email-sending.md#customizing-the-sending-method)
- [Custom settings and flags](./docs/custom-settings-and-flags.md)
  - [`EMAIL_CONFIRMATION`](./docs/custom-settings-and-flags.md#email_confirmation)
  - [`PASSWORD_RECOVERY`](./docs/custom-settings-and-flags.md#password_recovery)
  - [`TESTING`](./docs/custom-settings-and-flags.md#testing)
  - [`PRODUCTION`](./docs/custom-settings-and-flags.md#production)
- [Changelog](./CHANGELOG.md)
- [Licence](./LICENSE)

**See also:**

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
- [Django Guardian](https://django-guardian.readthedocs.io/en/stable/)
- [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

---
