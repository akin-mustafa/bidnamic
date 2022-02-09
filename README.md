# Bidnamic

## Stack
- Python 3.9
- Postgres 14.1


## Basic Principle

Program downloads and saves campaigns first, then process ad groups and search terms.
if a data has a related object that doesn't exist on database, the data will be ignored until related data is created


## Basic Commands

### Custom Management Commands
- to get all data use this command 

        $ python manage.py update_search_terms

- this command pull campaigns, ad groups and search terms by order


### Setting Up Your Users

-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy bidnamic

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run ./manage.py test .
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ python manage.py test .


### Celery

This app comes with Celery.

To run a celery worker:

``` bash
cd bidnamic
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

## Deployment

The following details how to deploy this application.
