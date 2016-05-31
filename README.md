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

```
brew install mongodb
python -m pip install pymongo
```

To run MongoDB server:

`mongod`

Login to MongoDB and create a new user:

```
mongo
use remanage
db.createUser({user: 'remanage', pwd: 'test', roles: [{role: 'dbAdmin', db: 'remanage'}]})
```
