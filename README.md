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