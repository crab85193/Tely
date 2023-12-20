# Tely

[![Docker](https://img.shields.io/badge/Docker-24.0.5-1488C6.svg?logo=docker&style=plastic)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11.0-3776AB.svg?logo=python&style=plastic)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.7-092E20.svg?logo=django&style=plastic)](https://www.djangoproject.com/)
[![Nginx](https://img.shields.io/badge/Nginx-1.21%20alpine-269539.svg?logo=nginx&style=plastic)](https://www.nginx.com/)
[![Twilio](https://img.shields.io/badge/-Twilio-F22F46.svg?logo=twilio&style=plastic)](https://www.twilio.com/en-us)
[![Sentry](https://img.shields.io/badge/-Sentry-FB4226.svg?logo=sentry&style=plastic)](https://sentry.io/welcome/)
[![Deploy](https://github.com/crab85193/tely-store-manager/actions/workflows/deploy.yml/badge.svg)](https://github.com/crab85193/tely-store-manager/actions/workflows/deploy.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

![logo](./docs/img/logo-w.png)

[日本語版はREADMEはこちら](./README.ja.md)

## Description
Repository of the proxy telephone reservation service [Tely](https://tely.st.ie.u-ryukyu.ac.jp/), which is produced by enPiT of the Intelligent Information Course, Department of Engineering, Faculty of Engineering, University of the Ryukyus.
Google Place API is used to obtain store information and Twilio is used to make outbound calls.

## Requirement
- Ubuntu22.04
- Docker 24.0.5
- Python 3.11.0
- Django 4.2.7
- Sentry-sdk 1.39.1
- twilio 8.10.0
- Google Place API

## Usage
Before starting Tely, you need to register to use [Google Place API](https://developers.google.com/maps/documentation/places/web-service/overview?hl=ja), create an account on [Twilio]( https://www.twilio.com/en-us), create an account on [Sentry](https://sentry.io/), create an account on [Outlook](https://www.microsoft.com/en/microsoft-365/ outlook/email-and-calendar-software-microsoft-outlook?deeplink=%2Fowa%2F&sdf=0).

After completing the above preliminary preparations, create `.env.dev` and write the following contents.

```
MYSQL_ROOT_PASSWORD={ROOT PASSWORD}
MYSQL_DATABASE={DATABASE NAME}
MYSQL_USER={USER NAME}
MYSQL_PASSWORD={USER PASSWORD}
MYSQL_HOST={HOST}
MYSQL_PORT={PORT}

SECRET_KEY=django
ALLOWED_HOSTS="*"

CSRF_TRUSTED_ORIGINS="localhost"

DEBUG=True

EMAIL_HOST="smtp-mail.outlook.com"
EMAIL_PORT=587
DEFAULT_FROM_EMAIL={OUTLOOK MAIL ADDRESS}
EMAIL_HOST_USER={OUTLOOK MAIL ADDRESS}
EMAIL_HOST_PASSWORD={OUTLOOK MAIL PASSWORD}

TWILIO_ACCOUNT_SID={TWILIO ACCOUNT SID}
TWILIO_AUTH_TOKEN={TWILIO AUTH TOKEN}
FROM_PHONE_NUMBER={FROM PHONE NUMBER}

GOOGLE_API_KEY={KEY VALUE}

SENTRY_DNS={SENTRY DNS ADDRESS}

```

After creating `.env.dev`, run the following command to start Tely.

```
$ docker-compose -f docker-compose.dev.yml up -d --build
```

## Reference

- [Python Documents](https://docs.python.org/3.11/)
- [Django Documents](https://docs.djangoproject.com/en/5.0/)
- [Google Place API Documents](https://developers.google.com/maps/documentation/places/web-service/overview?hl=ja)
- [Twilio Documents](https://www.twilio.com/docs)
- [Docker Documents](https://docs.docker.com/)

## License
Copyright © 2023 Team Quartetto Inc.

This software is released under the Apache 2.0 License, see [LICENSE](./LICENSE).
