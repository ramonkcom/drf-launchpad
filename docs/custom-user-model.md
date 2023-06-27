🔙 [Back to documentation](./index.md)

---

# Custom user model

From the [Django documentation](https://docs.djangoproject.com/en/dev/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project):

> If you’re starting a new project, it’s highly recommended to set up a custom user model, even if the default User model is sufficient for you.

This is not as trivial as it sounds, as you have to set a lot of things in place to make it work. So, to make things easier, this project already comes with an easy to extend custom user model, and all the necessary apparatus to make it work (configuration, related models, signals, custom manager etc).

- [The `User`, `Profile` and `Email` models](#the-user-profile-and-email-models)
- [The `core.signals`](#the-coresignals)
- [The `UserSerializer`](#the-userserializer)
- [The `UserFactory`](#the-userfactory)

---

## The `User`, `Profile` and `Email` models

The `User` model extends `django.contrib.auth.models.AbstractBaseUser` and differs from the default Django user model in the following ways:

- It does **not** have `first_name` and `last_name` fields, but has a `profile` field instead, which is a `Profile` model.
- It does **not** use `username` as the primary identifier, but uses `email` instead.
- It has `reset_token` and `reset_token` fields to support the password reset functionality.
- It has `emails`, which is a `Manager` of `Email` models, to support multiple emails per user.

The `Profile` model has a one-to-one (1:1) relationship to the `User` model, and it's meant to hold all the user's personal information. Here, it has only `given_name` and `family_name` fields, but can be extended to hold any other personal information such as picture, addresses, documents, phones etc.

The `Email` model has a many-to-one (N:1) relationship to the `User` model, and it's meant to hold the user's email addresses.

The Here's a summary of the models' fields:

### `User` Model:

- `id` (uuid): The unique identifier of the user.
- `date_joined` (datetime): The date the user joined the system.
- `email` (str): The primary email of the user.
- `emails` (Manager<Email>): Emails of the user.
- `groups` (Manager<Group>): The permission groups of the user.
- `is_active` (bool): Whether the user is active or not.
- `is_staff` (bool): Whether the user is staff or not.
- `is_superuser` (bool): Whether the user is superuser or not.
- `last_login` (datetime): The last login of the user.
- `profile` (Profile): The profile data of the user.
- `reset_token` (str): The token to reset the password of the user.
- `reset_token_date` (datetime): The date the reset token was generated.
- `user_permissions` (Manager<Permission>): The permissions of the user.
- `username` (str): The username of the user.

### `Profile` Model:

- `id` (uuid): The unique identifier of the user.
- `given_name` (str): The given name of the user.
- `family_name` (str): The family name of the user.

### `Email` Model:

- `address` (str): The email address.
- `confirmation_code` (str): The confirmation code.
- `confirmation_code_date` (datetime): The date the confirmation code was generated. Defaults to now.
- `confirmation_date` (datetime): The confirmation date.
- `origin` (str): The origin of the email. Defaults to 'USER_INPUT'.
- `user` (User): The user related to the email.

The `User` model is designed in a way that it partially hides the existence of its `Profile` in two main ways:

1. You can instantiate a `User` with `given_name`, `family_name` or any other `Profile` field as keyword arguments, and the `Profile` will be created automatically. For instance, both of the following statements are valid:

```
user_1 = User(given_name='John',
              family_name='Doe')

user_2 = User.objects.create(given_name='Jane',
                             family_name='Doe')

```

2. Using `user.given_name` to get or set a value is the same as using `user.profile.given_name`. Same applies to `family_name` or any other `Profile` field. For instance:

```
user = User.objects.create(given_name='John',
                           family_name='Doe')

print(user.given_name)  # 'John'
print(user.profile.given_name)  # 'John'
print(user.family_name)  # 'Doe'
print(user.profile.family_name)  # 'Doe'

user.given_name = 'Jane'
user.save()

print(user.given_name)  # 'Jane'
print(user.profile.given_name)  # 'Jane'

```

Notice that when extending the `Profile` model, you don't have to worry about somehow including the new fields in the `User` model: it will be done automatically through the magic methods. If you have problems in this regard, you can take a look in the implementation of `User`'s `__init__`, `__getattr__` and `__setattr__` methods.

---

## The `core.signals`

The `core.signals` module contains the signals necessary to make the custom user model work properly. The operations perfomed via signals are:

- The creation of a `Profile` for the `User` when it is created.
- The creation of an `Email` for the `User` when it is created.
- The creation of an unique `username` for the `User`, if `username` is not provided when the `User` is created.
- The assignment of the necessary permissions to the `User` when it's created.
- The assignment of the necessary permissions to the `User` when a new `Email` is created.
- The enforcement of the rule that `Profile` cannot be deleted directly.

---

## The `UserSerializer`

The `UserSerializer` is designed in a way that it hides the existence of the `Profile` and exposes its fields like they were fields of the `User` model.

However, the `ProfileSerializer` does exist and is used by the `UserSerializer` as the source of information about the `Profile` fields. This means that if you add fields to `ProfileSerializer`, they will be automatically exposed by the `UserSerializer`, so you don't have to worry about it. Of course, you can customize this behavior by modifying the `UserSerializer.get_fields` method.

---

## The `UserFactory`

It's important to notice two aspects of the `UserFactory`.

First, that it disables the signal that creates the `Profile` when a `User` is created, so you can take control of the strategy used to create a `Profile` for the `User`.

Second, that it overrides the `build_dict` method to include `Profile` fields in the dictionary as they were fields of the `User` model. The reason for this is that the API endpoints treat `User` and `Profile` as a single entity, so it's important that the `UserFactory` returns a dictionary with all the fields of both models to be useful in API tests.

As it happen with `UserSerializer`, you don't have to worry about it when extending the `Profile` model: the `UserFactory` will automatically include the new fields in the dictionary returned by `build_dict`. Of course, you can also customize this behavior by modifying the `UserFactory.build_dict` method.

---

🔙 [Back to documentation](./index.md)
