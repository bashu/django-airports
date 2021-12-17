Example Project for airports
============================

A script to painlessly set up a Docker environment for development of django-airports - inspired by [docker-wagtail-develop](https://github.com/wagtail/docker-wagtail-develop)

Setup
-----

**Requirements:** [Docker](https://www.docker.com/) and Docker Compose (Docker Compose is included with Docker Desktop for Mac and Windows).

Open a terminal and follow those instructions:

```sh
# 1. Decide where to put the project. We use "~/Development" in our examples.
cd ~/Development
# 2. Clone the django-airports repository in a new "django-airports-develep" folder.
git clone https://github.com/bashu/django-airports.git django-airports-develop
# 3. Move inside the new folder.
cd django-airports-develop/example/
# 4. Build the containers
docker-compose build
```

It can take a while (typically 15-20 minutes) to fetch and build all dependencies and containers.

Once the build is complete:

```sh
# 6. Start your containers and wait for them to finish their startup scripts.
docker-compose up
# 7. Now in a new shell, run the databse setup script. The database will be persisted across container executions by Docker's Volumes system so you will only need to run this commmand the first time you start the database.
./setup-db.sh
# Success!
```

If you're running this on Linux you might get into some privilege issues that can be solved using this command (tested on Ubuntu):
```sh
CURRENT_UID=$(id -u):$(id -g) docker-compose -f docker-compose.yml -f docker-compose.linux.yml up
```

- Visit your site at http://localhost:8000
- The admin interface is at http://localhost:8000/admin/ - log in with `admin` / `changeme`.

What you can do
---------------

### See a list of running containers

```sh
$ docker-compose ps
NAME      COMMAND                  SERVICE             STATUS              PORTS
web       "sh -c 'python manag…"   web                 running             0.0.0.0:8000->8000/tcp
```

### Run tests
```sh
docker-compose exec web python ./manage.py test airports
```

### You can open a django shell session

```sh
docker-compose exec web python manage.py shell
```

### You can open a shell on the web server

```sh
docker-compose exec web bash
```
