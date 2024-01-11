# Tely

[![Docker](https://img.shields.io/badge/Docker-24.0.5-1488C6.svg?logo=docker&style=plastic)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11.0-3776AB.svg?logo=python&style=plastic)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2.7-092E20.svg?logo=django&style=plastic)](https://www.djangoproject.com/)
[![Nginx](https://img.shields.io/badge/Nginx-1.21%20alpine-269539.svg?logo=nginx&style=plastic)](https://www.nginx.com/)
[![Twilio](https://img.shields.io/badge/-Twilio-F22F46.svg?logo=twilio&style=plastic)](https://www.twilio.com/en-us)
[![Sentry](https://img.shields.io/badge/-Sentry-FB4226.svg?logo=sentry&style=plastic)](https://sentry.io/welcome/)
[![Deploy](https://github.com/crab85193/tely/actions/workflows/deploy.yml/badge.svg)](https://github.com/crab85193/tely/actions/workflows/deploy.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache2.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

![logo](./docs/img/logo-w.png)

[English README is here](./README.md)

## Description
琉球大学工学部工学科知能情報コースのenPiTで制作している、代理電話予約サービス[Tely](https://tely.st.ie.u-ryukyu.ac.jp/)のリポジトリ。
Google Place API を使用して店舗情報を取得し、Twilioを使用して電話発信を行う。

## Requirement
- Ubuntu22.04
- Docker 24.0.5
- Python 3.11.0
- Django 4.2.7
- Sentry-sdk 1.39.1
- twilio 8.10.0
- Google Place API

## Usage
Telyを起動させる前に、[Google Place API](https://developers.google.com/maps/documentation/places/web-service/overview?hl=ja)の利用登録と、[Twilio](https://www.twilio.com/en-us)のアカウント作成、[Sentry](https://sentry.io/)のアカウント作成、[Outlook](https://www.microsoft.com/en/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook?deeplink=%2Fowa%2F&sdf=0)のアカウント作成を行なってください。

上記の事前準備が完了したら、`.env.dev`を作成し、以下の内容を記述する。

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

`.env.dev`作成後に、以下のコマンドを実行してTelyを起動する。

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