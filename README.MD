roles_api_pgsql
===========
Roles CRUD API

Quick Run
---------
```bash
cd roles_api_pgsql
pipenv install --dev && pipenv shell
cp .env.example .env
direnv allow
python setup.py install
```

For local development we strongly recommend using [direnv](https://direnv.net/)
Configure .env file or set OS environments:

* **listen_port** - Port, that app will listen
* **listen_host** - Host, that app will listen
* **db_name** - Database name
* **db_max_con** - Max database connection for poll
* **db_user** - Database user name
* **db_password** - Password for database user
* **db_host** - Host for DB instance
* **db_port** - Database port
* **log_level** - App's default log level

Run server with command:
```bash
roles-api-pgsql-ctl server run
# or with newrelic
newrelic-admin run-program roles-api-pgsql-ctl server run
```
