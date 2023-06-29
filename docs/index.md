# DRF Lauchpad - Documentation

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/Rest%20Framework-ff1709?style=for-the-badge&logo=django&logoColor=white)
![image](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white)
![image](https://img.shields.io/badge/Guardian-109989?style=for-the-badge&logo=django&logoColor=005949)
![image](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

DRF Lauchpad is a boilerplate for **quickly starting new RESTful API projects using Django and Django Rest Framework (DRF)**. It provides all the basic code and structure for developing RESTful API with Django and DRF.

- [Quick start](#quick-start)
- [Project structure](./project-structure.md)
  - [The `config` directory](./project-structure.md#the-config-directory)
  - [The `apps` directory](./project-structure.md#the-apps-directory)
  - [The `utils` directory](./project-structure.md#the-utils-directory)
  - [The `notebooks` directory](./project-structure.md#the-notebooks-directory)
- [Custom user model](./custom-user-model.md#custom-user-model)
  - [The `User`, `Profile` and `Email` models](./custom-user-model.md#the-user-profile-and-email-models)
  - [The `core.signals`](./custom-user-model.md#the-coresignals)
  - [The `UserSerializer`](./custom-user-model.md#the-userserializer)
  - [The `UserFactory`](./custom-user-model.md#the-userfactory)
- [Permissions](./permissions.md)
- [Email sending](./email-sending.md)
  - [Configuring Django mail system](./email-sending.md#configuring-django-mail-system)
  - [Customizing the email content](./email-sending.md#customizing-the-email-content)
  - [Customizing the sending method](./email-sending.md#customizing-the-sending-method)
- [Custom settings and flags](./custom-settings-and-flags.md)
  - [`EMAIL_CONFIRMATION`](./custom-settings-and-flags.md#email_confirmation)
  - [`PASSWORD_RECOVERY`](./custom-settings-and-flags.md#password_recovery)
  - [`TESTING`](./custom-settings-and-flags.md#testing)
  - [`PRODUCTION`](./custom-settings-and-flags.md#production)
- [Changelog](../CHANGELOG.md)
- [License](../LICENSE)

**See also:**

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
- [Django Guardian](https://django-guardian.readthedocs.io/en/stable/)
- [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

---

## Quick start

To start a new project using DRF Lauchpad, you basically just need to run the commands you would run to start any Django project. The only extra step is that you need to configure the email service of your choice to make the email related endpoints work. You can find the [instructions here](./email-sending.md).

### 1. Setup the project

After cloning DRF Lauchpad to your local machine, create a `.env` file in the root of the project. Set the following key-value pair on it:

```bash
DJANGO_SECRET_KEY="your-secret-key"
```

### 2. Install the requirements

Create a new virtual environment and install the requirements:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Make the migrations

Make the migrations and migrate the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run the project

Run the project:

```bash
python manage.py runserver
```

Then check the API at `http://localhost:8000/api/docs/`.

### 5. Configure the email service

In order for everything to work as designed, you need to set up an email sending service for sending email confirmation and password recovery emails. You can find the [instructions here](./email-sending.md).

### 6. Do your thing!

That's it. You good to start your project.

Most of the things in the project are obvious (like this instructions), but I highly recommend that you read the documentation to better understand the project structure and how things were designed to work.

Of course, you don't need to read all the sections from top to bottom. They are meant to be as independent from each other as possible so you can consult the sections as you go, according to your needs.

---
