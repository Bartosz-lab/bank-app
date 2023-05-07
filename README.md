# bank-app
Bank app for "Wstęp do Bezpieczeństwa Komputerowego" course

[![Deploy to DO](https://www.deploytodo.com/do-btn-white.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/Bartosz-lab/bank-app/tree/main&refcode=1ef7822c5071)

### After deploy
Go to Console tab and perform the Django first launch tasks:
* `python manage.py migrate` - This will perform your initial database migrations.
* `python manage.py createsuperuser` - This will prompt you for some information to create an administrative user.


## Deploy on Docker
Run `docker compose up -d --build`

### After deploy
Run this commands to perform the Django first launch tasks:
* `docker compose exec web python manage.py migrate --noinput` - This will perform your initial database migrations.
* `docker compose exec web python manage.py collectstatic --noinput` - This will collect all staticfiles.
* `docker compose exec web python manage.py createsuperuser` - This will prompt you for some information to create an administrative user.


Todo:
1. Add automatic customer group for new accounts
2. createuserform is it ok? self.error_messages["password_mismatch"] not defined
3. template for emails (auth_code and password reset)