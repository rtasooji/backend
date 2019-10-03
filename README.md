# Backend with django advance
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
    *   in docker-compose.yml add the command and migrate before running server.

##  Django in browser:
*   NOTE:
    *   Because we run django in docker make sure we are not using local host for 
        django app in docker use another ip address for the server
    *   We need to make super user for the admin inside terminal
```bash
docker-compose run app sh -c "python manage.py createsuperuser"
```

## User Management End point:

*   Adding --rm after run command in docker-compose will removes the container 
    after the command
*   We remove migrations, admin, models, and test files from new created app
    , the core app will handle this except fot test, we add test cases inside
    the tests foldres
*   in setting.py we add the newly created app, and adding `rest_framework,
    and 'rest_framework.authtoken'
*   the authentication token will be used to authenticate request to other API 
    in our project.
    
##  Adding test cases for user management:
*   for our test case we need to import some classes and functions:
    *   TestCase from django.test
    *   get_user_model function from django.contrib.auth
    *   reverse from django.urls
    *   APIClient from rest_framework.test, support for making API requests
        the class supports the same request interface as Django's standard
        Client class
    *   status from test_framework provides human readable http request
*   We added three test cases:
    *   user_create_successful
    *   no duplicate user 
    *   weak password with less than 5 chars
*   Also we added helper function and const variable for testing.
*   Made payload and send payload as post command with the url
*   check the result respond's status.
    *   the respond for create HTTP_201
*   after creating we user our model to get the user and check the password
*   the res.data shouldn't have any password info in it
```python
res = self.client.post(URL, payload)
self.assertNotIn('password', res.data)
``` 
*   For duplicate test case we check the post response status is 400
*   For short password after checking for 400 response, we need to check
    no user is created in our database
```python
user_exist = get_user_model().objects.filter(email=payload['email']).exists()
self.assertFalse(user_exist)
```
## Add Create User API:
*   There are three steps required to create the api
    *   create a serializer for creating user request
    *   creating a view to handle the request
    *   Wire up the view to a URL, which allows us to access the API
*   Serializing in django:
    *   creating a serializers.py file inside the app
    *   include serializer from rest_framework
        * Inherent ModelSerializer from serializer
    *   Adding class Meta
        *   defining the model we are using in model variable
        *   defining the fields that we want to convert to and from json
            when we make our HTTP post request, then we retrieve it to 
            our view and save it to our model. In another word, fields
            we want accessable in our API either read or write
        *   extra_kwargs, allows us to configure extra settings in our model
            serializer and we are going to make sure the password is write_only
            and min_length is 5 chars.
    *   defining create function to pass the validated data after serializing
        into our model create_user function
*   Adding view for managing our create user API:
    *   update view.py file in our app folder
    *   import our UserSerializer we just created
    *   import generics from rest_framework, this provides a generic
        class for Creating View for API
    *   inherent generics.CreateAPIView, and just point 
        serializer_class variable to our UserSerializer
*   Adding URL and wiring URL to our view:
    *   in app folder create urls.py
    *   import our view.py from app folder
    *   import path from django.urls, this will helps us to define 
        different path in our model which can be used by reverse function
    *   Define app name inside app_name variable this will be used in reverse
        as first parameter
    *   define urlpatterns list variable
        *   the element inside list is path, which will be pointed to our view
    ```python
    urlpatterns = [
        path('create/', views.CreateUserView.as_view(), name='create'),
    ]
    ```
    *   import include from django.urls 
    *   in urls.py in main app folder, we will include the new created urls.py
    ```python
    urlpatterns = [
    .
    .
    .
    path('api/user/', include('user.urls')),
    ]
    ```
    *   Any request starts with api/user will go to user.urls and from
        there it checks the next part.
        For create it checks create, then it calls the view
        from view it calls the serializer class, serialize the json format,
        and pass the validated data to create_user model.
        
## Adding test for create token API:
*   This is an end point to make HTTP post request and generate a temporary 
    authentication token that can be used to authenticate future requests
    with the API, so we don't need to send username and password with every 
    request.
*   We provide the generated token as authentication header for future request.
*   We can store the token in cookie or persistent storage that we can use
    to authenticate in future.
*   We can revoke (put an end) the token in database at any time in future 
*   Four unit test provided:
    *   check successful generated token
    *   check invalid credentials
    *   check not generated user
    *   check empty password for generated user
    ```python
    # check if key not available inside the respone
    self.assertNotIn('token', res.data)
    ```
## Adding Create Token API:
*   in serializer:
    *   Make AuthTokenSerialzier class inhereted from serialize.Serializer
    *   import authentication function from contrib.auth
    *   import ugettext_lazy as _ from utils.transloation
        *   This is being used for converting language if in needed
        *   the different between this and get_text is not explained
    *   when calling validation function we check the credentials are correct
    *   if they are correct we return them, when calling the validate 
        function we need to return attr parameter at the end
    ```python
    class AuthToken(serializer.Serializer):
        email = serializers.CharField()
    
        # by default django trim whitespace 
        # we want to include white space in password at start and end
        password = serializers.CharField(style={'input_type': 'password'},
                                         trim_whitespace = False)
        def validate(self, attrs):
            email = attrs.get('email')
            passwrod = attrs.get('password')
    
            #   Get access to the context of the request that was made
            #   What djngo does when request is made it pass it to the 
            #   serializer in the context class variable
            user = athenticate(request=self.context.get( 'request' ),
                                username=email,
                                password=password)
            if not_user:
                msg=_('Unable to authenticate with provided credintial')
                raise serializer.ValidationError( msg, code='authenticateon')
            user['user'] = user
            return attr
    
    ```    
    
## Adding test to manage user endpoint:
*   This endpoint allows the authenticated user to update their own profile,
    including changing name, password and viewing their user object.
*   new const url ME_URL with {user:me} added
*   4 test cases added to test_user_api:
    *   Test the authentication is required to be able to change
        *   this test implemented in public, because authenticated user is 
            not required
    *   Retrieving authenticate user is successful 
        *   a new class with new setup created.
        *   the setup has:
            *   user, client, force_auth user to client 
        *   check self.client.get(ME_URL)
        *   return status should be 200
        *   data has name and email only, no password should be included
    *   http post is not allowed:
        *   Post is for creating, push and patch is for editing
            *   Push vs Patch:
                *   PUT method only allows a complete replacement of a document
                *   PATCH request is used to make changes to part of the 
                    resource at a location, that is it patches the resources,
                    changing its properties. It is used to make minor updates
                    to resources
                *   If resource is not available, the patch fails without
                    creating a new resource, unlike PUT which would
                    create a new one using the payload
        *   send Post request
        *   the response from the post should be 405 (method not allowed)
    *   test user profile is updated
        *   make new payload
        *   patch the new payload
        *   update user with self.user.refresh_from_db()
        *   assertEqual(self.user.name, payload['name'])
        *   assertTrue(self.user.check_password(payload['password]))
        
## Adding Manage User Endpoint:
*   in serializer.py
    *   in class UserSerializer we override update function
    *   The purpose for this is to make sure the password is set using the 
        set_password function instead of just setting it to whichever value 
        is provided
    *   The instance parameter of update function is the model instance that 
        is linked to our model serializer will be user object.
        Validated_data parameter are data in Meta class and ready for validation
    ```python
    password = validation_data.pop('password', None)
    # call the update from super class which is ModelSerializer 
    user = super().update(instance, validated_data)
    if password:
        user.set_passwrod(password)
        user.save()
    return user
    ```
*   in user/view.py:
    *   import authentication and permission from rest_framework
    *   Add ManageUserView class inhereted from generic.RetrieveUpdateAPIView
    *   define serializer_classes
    *   define authentication_classes this needs to be iterable like list or tuple
    *   define permission_classes
    *   We need to overwrite get_object function, in our case we only want to 
        retrieve model for the logged in user, so we return the authenticated user
    ```python
    class ManageUserView(generic.RetreiveUpdateAPIVIEW):
        serialization_classes = UserSerializer
    
        # this will define the mechanism authentication will happen
        authentication_classes = (authentication.TokenAuthentication, )
    
        # Permission is the level of access that the user has 
        #   The user is authenticated to use api they don't have to have any
        #   specific permission just logged in
        permission_classes = (permission.IsAuthenticated, )
        
        def get_object(self):
    
            # When the object is called the request will have the user, attached
            # to it because of authentication_classes, thiw will authenticate
            # user and attach it to the request.
    
            return self.request.user
    
    ```
            