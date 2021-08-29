## Village

### Prerequisites

```
python3 (3.7.5)
pyenv
pipenv
PostgreSQL 11.5
```

## Clone the repo
```
git clone git@github.com:village/village.git
```

## Use Python 3.7.5
```
brew install pyenv
brew install pipenv
pyenv install 3.7.5
pyenv shell 3.7.5
```

## Installing Postgresql
As of this Readme the latest stable version of Postgres is 11.5. Therefore running the following `brew` command should suffice.
However, it is always a good idea to check this website to make sure that the latest is in fact 11.5. If there is a newer version available you may need to add a suffix like so- `postgresql@11`.

https://formulae.brew.sh/formula/postgresql

```
brew install postgresql
```

Then install the dependicies (make sure postgresql is installed before):

```
cd village
pipenv install --dev
```

If you get an error regarding zlib, following instructions here: https://github.com/jiansoung/issues-list/issues/13

Add the following lines to always be in python 3.7.5 to your .bash_profile and .bashrc file

```
eval "$(pyenv init -)"
pyenv shell 3.7.5
```


## Developing on the backend

### Database connection:
create a village database:
don't have postgresql installed? Refer to the section above titled "Installing Postgresql"

```
brew services start postgresql
psql -d template1
create database village;
\c village ;
```

If you see an `address already in use error` when trying to run `brew services start postgresql`, try
```
brew services list
brew services stop (OLD POSTGRES)
```

Run migrations:
```
FLASK_ENV=development pipenv run flask db upgrade
```

### Start local server
```
cd village
FLASK_ENV=development pipenv run flask run
```
* go to: http://localhost:5000/

If you're using pyenv, you might need to specify the path to the python executable
installed through pyenv. You can get the path by doing:
```
pyenv which python
```

You can also add `FLASK_ENV` to your environment variables by adding
```
export FLASK_ENV=development
```
to your `.bash_rc` or `.zshrc`.

Don't have selenium?
```
brew cask install chromedriver
```


### Add dependencies
```
pipenv install <pip-package>
```

### Schema migrations
Update the model, then run
```
FLASK_ENV=development pipenv run flask db migrate -m 'YOUR COMMENT HERE'
```
to generate the alembic migration. *Make sure to glance at the auto-generated migration
file to double check that it's not unexpectedly going to drop anything.* Computers
aren't perfect! If you're connected to a local database, run
```
FLASK_ENV=development pipenv run flask db upgrade
```
to apply the migrations.

**Note**: `FLASK_ENV=development` tells flask to run using local config. If you're developing against the staging
database, running the `upgrade` command locally without rolling it back will likely cause
the migration to fail during deploy.

If you're developing against the production database, maybe just...don't.

##  Developing on the client side

### Install dependencies
```
cd client
yarn install
```

### Start local server
```
yarn start
```

### Create production build
```
yarn build
```

* All the files are generated beforehand to serve the flask app, so you have to build them in order to see any changes


### RabbitMQ:
RabbitMQ is a message-broker software that implements the Advanced Message Queuing Protocol (AMQP)
to install it:
```
brew install rabbitmq
brew services start rabbitmq
```
the go to the default local url:
```
http://localhost:15672/#/
```
type in guest, guest


### Celery:
Celery is an asynchronous task queu.
We use it, for example, to connect with different loan providers. It should be installed with regular python dependencies

On local, open a new terminal and run:
```
FLASK_ENV=development pipenv run celery worker -A tasks --loglevel=info
```

### Run test

To run tests enable the virtual environment

Then run:

```
FLASK_ENV=testing pipenv run pytest .
```

or

```
FLASK_ENV=testing pipenv run pytest controller services models third_party tests recommendation_engine
```
which is faster



### Pre-commit

```
pip install pre-commit
pre-commit install
```
enjoy