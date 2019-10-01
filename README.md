# 23, Sep, 2019
* Setting up project repository for udemy backend course

## notes:
* The docker file is a list of instruction for docker to build our docker image.
  *  We describe all the dependencies for the project in the docker file.

## Notes on Dockerfile:
* The first line of the docker file is the image that we are going to inherent from
* We can build our docker file on top of image with python in it!
  * go to docker hub
  * look for python
  * we are looking for "3.7-alpine"
    * alpine means a lighter version of docker and it runs python 3.7
    * ENV PYTHONUNBUFFERED:   means to run python in unbufferen mode which is recommended
      when using python with docker containers.
      It doesn't allows python to buffer the output and prints them directly.
      Which will avoid some problem when running docker application with python.
    * copy from requirments.txt from project to docker image requirments.txt
    * Creates /app in docker image, make it as workdir and copy from ./app in project
      to /app in docker image
    * adduser -D (D means users that only can run the application)
    * User user: switch the docker to user that we created.
      * For security purposes we don't give them root access to the project

## Notes on requirements.txt
* check the latest version of django from pypi and add it and other dependencies that are needed

## Notes on building Docker
* we add the app folder in the project
* in terminal we run

```bash
docker build .
```
## Notes on docker compose
* docker compose is a tool that allows us to run the docker image easily from our
  project location.
  * allows us to manage different services that makes our project
    * one server runs the python app
    * one server runs the database
*   the first line on docker-compose file is the version of docker compose
* we will have a service called app, and the build section of the configuration,
  we are going to have a context to ".", which is our current directory.
* port 8000 on our host to 8000 on our image
* volumes allow us to get the update we make to our project in to our docker image
  in real time
* command: > will add line in next line, make sure to start it one space after indentation
* sh -c : sh is shell command and c is command

## Notes on creating django project
*  Using the docker configuration that we created
* Use docker compose to run a command on our image that contains django dependencies.
  This will create the project file we need for our app.
```shell
docker-compose run app sh -c "django-admin.py startproject app ."
```
runs django-admin management command that comes when we install django, then it runs
the start project command and installs a new project called app and start it in
our current location.

# 25, Sep, 19

## Notes on Travis:
* Add .travis.yml file in the project
* Pipeline for bitbucket and jenkins are other option for CI (Continous Intergration)
  [here]{guru99.com/jenkins-vs-travis.html} a link for comparing jenkins vs Travis

## Notes on flake8:
* For configuring flake8, we add a file inside django app folder with name .flake8
* adding exclude to django files because they are not following pep standard such as
  79 characters per line

## Notes on Unit Test:
* Django looks for any file starts with test name
* We need to import django TestCase module
* The test function needs to start with test too
* The command to run the test inside docker container
```bash
docker-compose run app sh -c "python manage.py test"
```

# 28, Sep, 19

## Notes on Core APP:

* Handles every essential parts that are important for sub apps
* Creates anything that needs to be shared between one or more apps, things such
  as migration, database,...
* To create core app:
* core vs project:
  * an App is a web application that does something, this can be database, weblog,
    or a simple poll. An app can be in multiple projects.
  * A project is a collection of configuration and apps for a particular website.
    A project can contain multiple apps.
```bash
docker-compose run app -sh -c "python manage.py startapp core"
```

## Notes on django contrib and user model:
* {Link}[https://docs.djangoproject.com/en/2.2/ref/contrib/] to contrib package
* Instead of referring to User directly, you should reference the user model
  using django.contrib.auth.get_user_model().
*   Making custom user model to have email as username.
    *   Define the test case, the test case requires user name but our model requires only
        email
    *   in models.py in core app we define tue manager and the class
    *   in setting.py at the end we define the model
    *   in setting.py at INSTALLED_APPS we add our app.
*   To create the model:
```python
python manage.py makemigrations "name of the app"
```
*   The command will make a file in migrations folder that tel django how to make the database
*   Super user: super user is a function used by the django CLI when we are creating
    new user using the command line, so we add it to make sure we can use the features
    that comes with super user inside django

## Notes on Django admin
*   Setting admin will give us a nice easy interface that we can use to log in
    and see which users have been created, create user, or make changes to 
    existing users.

*   Adding test case for admin
    *   helper functions: reverse from django.urls, Client from TestCase, 
        get_user_model from Auth
    *   setUp the test case pay attention to setUp to correctly overwrite the function
        *   make client, make admin user, force-login to client, make reg user
    *   Make test function:
        *   use reverse to generate url
        *   pass url to client
        *   assertContaine the returned object for value we are looking for
    
*   Setting up admin.py
    *   import default AdminUser from conrib.auth and inherent the class
    *   change the values to other things
    *   register the custom model to the new UserAdmin 

*   Setting up fieldset:
    *   Set fieldset to control the layout of admin _add_ , _change_ , __Create__ pages
    *   We need gettext function from translate in case we want to add multiple
        language it is good to have it import it as "_"
    *   Look at the format of fieldset
    *   Question: How to add extra field and make it work?
        *    adding 'date_joined' to important-date field will not pass the test

*   Setting up add_fieldset:
    *   There is a separate field set for add
    *   This also needs to get overwritten to work with user without username
        *   add_fieldset needs to be changed

## Notes on setting up databse:
*   set up docker-compose.yml
    *   add db to service
    *   db has image of postgres from docker container
    *   we add the environment variable for db
    *   in app service we set up environment for app 
    *   We need to connect the dependency for our app service 
        *   when making docker-compose, we can create different services
            that depends on other services
        *   these dependencies will start before the app
        *   the services will be available through network with this service
        *   to do so:
            *   depends_on
*   set up docker file and requirement.txt
    *   Django recommend to use "psycopg2" as a package to connect with 
        postgresql
    *   We add the package to the requirement.txt
    *   The package requires some dependencies to work
    *   We add the dependeincies to install inside Dcokerfile before running
        pip command
```bash
## update: update registery before adding
## no-cache: Dont store registry index on dockerfile to make sure 
## the docker file is small and minimize security issues

RUN apk add --update --no-cache postgresql-client 

## --virtual: allows us to use these dependencies to install psycopg2 on docker
##  and remove them later on to minimize the size of the docker

RUN apk add --update --no-cache --virtual .tmp-build-dep \
    gcc libc-dev linux-headers postgresql-dev
.
.
.

# After running pip install -r requirement.txt, we are removing the dependencies
RUN apk del .tmp-build-dep 


```
*   Set up django to work with postgresql:
    *   in setting.py in DATABASE section:
        *   Change ENGINE to postgresql
        *   By using environment vairalbe we can easily call the database
            inside our project by using os.environ.get("Name of the env")
        *   We defined the name of env in our docker-compose
        
## Docker vs Docker-Compose:
*   Compose is a tool for defining and running multi-container Docker applications
*   We define the services inside YAML file and create and start all services.
*   Dockerfile is used to be able reproduce the app anywhere
    *   In our project the app service uses an image that's built from 
        the Dockerfile in the current directory
    *   the db service uses the public image postgresql 

## Mocking
*   Mocking is an advance area in testing  to override or change the behavior of 
    dependencies
* Why mocking:
    *   We don't want our test depends on external services
*   with mocking we:
    *   Isolate the specific piece of code
    *   Avoid un intended side effects
*   For example if we want to test email functionality we don't want to send 
    email every time. we use mocking to override the dependencies that sends 
    email and replace it with mocking object.

## writing test class for command:
*   python unittest.mock import patch provides mocking functionalities
*   django.core.management import call_command gives access to command inside 
    source code
*   django.db.utils import OperationalError simulate the raise error accessing 
    database
*   using patch in test function:
```python
with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
    gi.return_value = True
    self.assertEqual(gi.call_count, 1)
```
 *  Patch will do two things:
    *   Change the behavior of function
    *   Check how many times it being called or different calls were made to it
*   We can use patch as decorator for test method.
    *   if in our method we need to wait 5 seconds we can disable the time 
    *   It needs to be passed to method as parameter
```python
@patch('time.sleep', return_value=True)
def test_db_wait(self, ts):
    with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
        gi.side_effect = [OperationError] * 5 + [True]
        self.assertEqual(gi.call_count, 6)
```
*   Patch side_effect we can pass a list of Errors or value to returned through 
    iteration.
## Adding command to django:
*   To add custom command:
    *    create package management inside app
    *   create package commands inside management
    *   create module with the name of the command inside commands
    *   We need to inherent BaseCommand class from django.core.management.base
    *   We raise OperationError if database is not available from
        django.db.utils 
    *   To connect to the database we import connections from django.db
    *   the abstract function handle needs to be implemented from BaseCommand
    *   The BaseCommand has stdout.write function to output on terminal
    *   self.style.SUCCESS("Nice") can be used to output in green
    *   connections["default"] to connect to default database setup in setting.py