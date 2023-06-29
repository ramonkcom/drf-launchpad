# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2023-06-29

### Added

- `load_entity` helper function
- `config/settings/django_email.py` for email settings
- `EMAIL_CONFIRMATION['FRONTEND_BASE_URL']` setting
- `PASSWORD_RECOVERY['FRONTEND_BASE_URL']` setting
- `EMAIL_CONFIRMATION['SEND_EMAIL_IN_DEV']` setting
- `PASSWORD_RECOVERY['SEND_EMAIL_IN_DEV']` setting

### Changed

- `PASSWORD_RESET` setting is now `PASSWORD_RECOVERY`
- `EMAIL_CONFIRMATION['SEND_CALLBACK']` setting is now `EMAIL_CONFIRMATION['SEND_EMAIL_CALLBACK']`
- `PASSWORD_RECOVERY['SEND_CALLBACK']` setting is now `PASSWORD_RECOVERY['SEND_EMAIL_CALLBACK']`
- Emails are now sent using Django mail system by default

### Removed

- `EMAIL_CONFIRMATION['DEFAULT_FROM']` setting

## [0.0.1] - 2023-06-27

### Added

- Initial version
- README
- Documentation
- CHANGELOG
- LICENSE
