# Ortelius

Data server and API for handymap

## Setting up project for development

### Requirements

* Python ≥ 3.6
* Falcon
* Hug
* SQLAlchemy
* GeoAlchemy2
* Shapely
* Alembic
* Coverage python module
* PostgreSQL 9.4
* Geos
* PostGIS

### Setting up

#### Installing dependencies on Fedora Linux

```bash
sudo dnf install gcc gcc-c++ make glibc-headers python3 python3-virtualenv python3-devel python3-psycopg2 postgresql postgresql-devel postgresql-server postgresql-contrib libffi-devel redhat-rpm-config geos postgis
```

#### Setting up python environment:

Create virtual python environment:

```bash
cd path/to/your/project/folder
virtualenv-3.4 ortelius_env
```

where ortelius_env — name for your virtual environment for this project.

Switch to this environment:

```bash
source ortelius_env/bin/activate
```

Install project Python dependencies:

```bash
pip install -r requirements.txt
```

##### Start PostgreSQL database server:

```bash
sudo postgresql-setup --initdb
sudo systemctl start postgresql
```

Now we need to create database for development.
First, we need to create user in database, which will be used by our app for access to db.
Switch to postgres user and open postresql console for initial setup:

```bash
sudo -iu postgres
psql
```

In postgres console:

```sql
CREATE USER hm WITH password 'hm';
CREATE DATABASE hm;
GRANT ALL privileges ON DATABASE hm TO hm;
ALTER USER hm WITH SUPERUSER;
```

*Note, if you want to use other user instead of "hm", you need to change "hm" on your username and password in Handymap configuration file `settings.py`*

After that, exit psql console by pressing Ctrl+D and log out from user postgresql (Ctrl+D).
Next, open file `/var/lib/pgsql/data/pg_hba.conf` under root user, for example:

```bash
sudo nano /var/lib/pgsql/data/pg_hba.conf
```

In the end of file you can see smtg like:

```bash
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
```

change `local all all peer` to `local all all md5` to enable password authentication for users created only for postgresql.
It could be smtg like:

```bash
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     md5
```

After that, save file and restart PostgreSQL server:

```bash
sudo systemctl restart postgresql
```

Enable autostart PostgreSQL database server on system boot:

```bash
sudo systemctl enable postgresql
```

Done! =)

## Development server

Use ./manage.py script to manage development server

Create database schema:

```bash
./manage.py create_db
```

Delete all information in database:

```bash
./manage.py drop_db
```

Create database initial data:

```bash
./manage.py create_data
```

Create migration:

```bash
./manage.py migrate
```

Update database schema to migration:

```bash
./manage.py upgrade
```

Start development server:

```bash
./manage.py run
```

Deploy to heroku:

First, install heroku toolbelt.

For deploy from master branch, type:

```bash
./manage.py deploy
```
