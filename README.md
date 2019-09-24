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
* volume allow us to get the update we make to our project in to our docker image
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
