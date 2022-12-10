# Web Services - Theodor-Alin Oprea - 341C1
Time to implement: ~25h

## General Info
The webservices have been implemented using Django for the API, PostreSQL for
the DB and pgadmin for an auxiliary interface to manage the DB. More than
that, Django has a useful built-in interface for the same thing, the Admin
View, in which the user can easily access the DB in a very intuitive GUI.

## Project Structure
In the root of the project are 2 files used to build and run the containers,
the Dockerfile which builds the API container, and the docker-compose.yml
file, used to run the project. In the docker-compose file, there are 3
services run, the API, the DB and the PGAdmin interface.

Both the API and the PGAdmin interface depend on the DB service, the API is
forced to wait until the DB is fully up and running, thus the used while
loop. The services are all named, so they can be accesed using the names of
the services, `api`, `db` and `pgadmin`. The ports can be easily configured
from the docker-compose files, since the API uses environment variables, not
hardcoded values (the ENV variables will have to be updated in the `.env`
file to be updated in the `API` container as well).

Since a more well defined network is desired, the `api` and the `db` share a
network of theirs, as well as the `pgadmin` and the `db` containers. The
result is that the `api` and the `pgadmin` containers cannot communicate,
leading to a better independency of the containers.

The API is made of one base endpoint, the 'Master' endpoint, which routes
request to the 3 main endpoints of the project, the Country Endpoint, the
City Endpoint and the Temperature Endpoint.

The DB tables are defined in each Country, City, Temperature module, in the
models directory, as a class inheriting models.Model class, an ORM, making it
a lot easier to work with the database. In order to actually create the
databases, I have generated the migrations files for each table, migrations
which are run at the startup of the API container, using the
`python3 manage.py migrate` command.

## Setup / How to Run
To start the project, the user has to run the following command in the root
of the project:
```
docker-compose up --build
```
The `--build` option is used to build the images for the needed containers,
the API container, the DB container and the PGAdmin container.

In order to acces the PGAdmin interface, simply navigate to the following
address in a browser:
```
localhost:5050/
```
and use `admin@admin.com` and `admin` as credentials.

In order to access the Django Amin interface, the user has to firstly create
an 'admin' user inside the API container, by running the following commands:
```
docker-compose exec api bash
python3 manage.py createsuperuser
```
when prompted, insert whatever email, username and password are desired. If a
basic combination is used, something like `username: root, password: root`,
you will be asked if you want to keep the combination, due to the weakness
of the security of the account. After the superuser is created, open a browser
and navigate to the page:
```
127.0.0.1:8000/admin/
```
and when prompted, insert the used credentials for the super user account.

## Checker
For the user to check the functionality of the project, they need to import
the `TestAPI-Tema2_2022-2023.json` file in Postman, set the `PORT` variable
to whatever port the user configures in the docker-compose.yml file, or 8000
by default, click on `Run Collection`, rearrange the requests in the following
order:
- Add Country v2
- Get Country v2
- Add City v2
- Get City v2
- Get Cities by Country v2
- Add Temperatures
- Get Temperatures By Lat
- Get Temperatures By Lat and Lon
- Get Temperatures By Incorrect Temperature
- Get Temperatures By Correct Temperature
- Get Temperatures By City
- Get Temperatures By Country
- Put Temperature
- Delete Temperature
- Put City v2
- Delete City v2
- Put Country v2
- Delete Country v2

and click `Run Tema2 SPRC`
