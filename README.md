# darkweb

This used to be the repository holding the DarkScience website, that has been
moved to https://git.drk.sc/darkscience/darkscience.net.

At the moment this repository contains a Django application which powers the
quotes system for DarkScience. This is a legacy part of the old website still
in service.

## Development Environment

You can configure a development environment with the following:

**NOTE**: *These steps assume you have Python 2 along with virtualenv installed.*

You will need to install postgresql library beforehand, this can be accomplished
on macOS/Homebrew as `brew install postgresql`. For development purposes you
could also comment out the dependency in `requirements.txt` though.

```bash
$ virtualenv venv
$ source venv/bin/activate # add .fish for fish users
$ pip install -r requirements.txt
$ pip install mock
# configure URL to DB (can be sqlite locally)
$ export DATABASE_URL="sqlite:///$(pwd)/db.sqlite"
$ python manage.py syncdb
$ python manage.py migrate
```

### Running the tests

```bash
$ python manage.py test
```

### Running the development server

```bash
$ pipenv run python manage.py runserver
```

