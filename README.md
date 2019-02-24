
TODO:
        Use pip-tools to configure dependencies:
        https://stackoverflow.com/a/35411399/41829


        Pagination: Use digg style/google style (endless) pagination
        http://django-el-pagination.readthedocs.io/en/latest/index.html

## Development
1. run `redis-server`
2. Activate the virtualenv `env\Scripts\activate.bat`
2.a. Install the requirements `pip install -r production\requirements.txt`
3. run `python manage.py runserver`.

## Run as production
`DJANGO_SETTINGS_MODULE=dj.settings.production python3 manage.py runserver`

## Deploying
New:
- git push heroku master

Old:
Run fab from the host machine:

- `ssh i.jmnorlund.net`
- `sudo su - fedry`
- `cd ~/dj && fab production deploy`


   Use the above command to deploy with production settings to the production site.
