#Getting Started

 - `pip install virtualenv`
 - `virtualenv venv`
 - Open the `venv/bin/activate` file
 - Export some env variables at the end of the file :
   - `export DJANGO_SETTINGS_MODULE='malanimals.local_settings'`
   - `export MALANIMALS_SECRET_KEY='some_string_key'
   - `export MALANIMALS_DEBUG=1`
 - `source venv/bin/activate`
 - `pip install -r requirements.txt`
 - `python manage.py migrate`
 - `python manage.py runserver localhost:8000`

**Mananement command**
You can run `python manage.py stresstest` to add 1000 animals in the database in order to test the front-end consumming this API. This command take one of two possible arguments:
 - `--total` : followed by the total number of animals you want to add : `python manage.py stresstest --total=10000`
 - `--reset` : removed all animals from database : `python manage.py stresstest --reset`

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

 You can then toy with the management command stated above, you'll just need to to run them inside an `heroku run` command : `heroku run "python manage.py stresstest"`