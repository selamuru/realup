# Realup

Real estate management tool

## Development Environment Setup

### Install Python 3

```
brew update
brew install python3
```

### Install pip

`pip install -U pip`

If `pip` now fails with: "pkg_resources.DistributionNotFound: pip==1.5.6", run:

`easy_install --upgrade pip`

### Install & Use VirtualEnv

`pip install virtualenv`

To activate virtualenv run the following from project root:

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

To deactivate virtualenv run the following from project root:

`deactivate`

### Install & Run MongoDB

Run `deactivate` if you're currently running virtualenv.

```
brew install mongodb
python -m pip install pymongo
```

To upgrade pymongo:

`python -m pip install pymongo --upgrade`

To run MongoDB server:

`mongod`

Login to MongoDB and create a new user:

```
mongo
use remanage
db.createUser({user: 'remanage', pwd: 'test', roles: [{role: 'dbAdmin', db: 'remanage'}]})
```

### Running server and tests locally

To run the server locally, make sure you're in the virtual environment and run the following:

`python manage.py runserver`

To run the tests locally, make sure you're in the virtual environment and run the following:

`./manage.py test remanage.tests`

### Populating Local DB with Seed Data

To clear all existing data in DB and create fresh data from the seed files, run the following:

`python manage.py populate_seed_data -c`

To keep existing data in DB and add additional data from the seed files, omit the -c option:

`python manage.py populate_seed_data`