#Getting Started

 - `pip install virtualenv`
 - `virtualenv venv`
 - Open the `venv/bin/activate`
 - add at the end of the files, export some env variables by writing the following lines :
   - `export DJANGO_SETTINGS_MODULE='malanimals.local_settings'`
   - `export MALANIMALS_SECRET_KEY='some_string_key'
   - `export MALANIMALS_DEBUG=1`
 - `source venv/bin/activate`
 - `pip install -r requirements.txt`
 - `python manage.py migrate`
 - `python manage.py runserver localhost:8000`

 **Configuration**

You might to edit the `malanimals/local_settings.py` file to set different configuration option for using other kind of database for example (default one is sqlite3)

#Deployment

 - `heroku create`
 - `heroku addons:create heroku-postgresql:hobby-dev`
 - `heroku config:set DJANGO_SETTINGS_MODULE='malanimals.heroku_settings'`
 - `heroku config:set MALANIMALS_SECRET_KEY='some_random_secret_key'`
 - `heroku config:set MALANIMALS_DEBUG=0`
 - `heroku config:set DISABLE_COLLECTSTATIC=1`
 - `git push heroku master && heroku run "python manage.py migrate"`