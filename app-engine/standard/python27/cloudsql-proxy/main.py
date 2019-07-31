from flask import Flask, request, render_template, session
from functools import wraps

import sqlalchemy
import pymysql
import pymysql.cursors

import os

app=Flask(__name__)

app.secret_key="cloudsql"

instance_name=os.envorin.get(INSTANCE_CONNECTION_NAME, 'project:location:name')

@app.route('/')
def index():
    data = {'headers':      request.headers,
            'service_name': os.environ.get('CURRENT_MODULE_ID', '(running locally)'),
            'environment':  os.environ}
    return render_template('index.html', data=data)


def requires_root_credentials(func):
    @wraps(func)
    def get_root_credentials(*args, **kwargs):
        if 'user' not in session:
            user = request.args.get('user', None)
            password = request.args.get('password', None)
            print(user, password)
            if user and password:
                session['user'] = user
                session['password'] = password
            else:
                return "No provided credentials", 401
        return func(*args, **kwargs)
    return get_root_credentials


@app.route('/create_table')
@app.route('/create_table/<database>')
@requires_root_credentials
def create_table(database='test'):
    if database:
        try:
            db = sqlalchemy.create_engine(
                    sqlalchemy.engine.url.URL(
                        drivername='mysql+pymysql',
                        query={
                            'unix_socket': '/cloudsql/{}'.format(instance_name),
                        },
                        username=session['user'],
                        password=session['password'],
                        database=database
                    ),
                    pool_size=15,
                    pool_timeout=30,
                    pool_recycle=1800
                )
        except Exception as e:
            return "There was an error while creating the connection. Error " + str(e)

        try:
            with db.connect() as conn:
                conn.execute(
                        "CREATE TABLE IF NOT EXISTS {} ".format(database) +
                        "(name VARCHAR(20), surname VARCHAR(25), " +
                        "age SMALLINT, user_id SERIAL, PRIMARY KEY(user_id))"
                    )
                return "Created database {}".format(database)

        except Exception as e:
            return "There was an error while creating the table. Error: " + str(e)

    return "Database {} already created".format(database)

 
@app.route('/create_database_pymysql')
@app.route('/create_database_pymysql/<database>')
@requires_root_credentials
def create_db(database='test'):
    if database != 'test':
        conn = pymysql.connect(
                        unix_socket='/cloudsql/{}'.format(instance_name),
                        user=session['user'],
                        password=session['password'],
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor
                    )

        try:
            csr = conn.cursor()
            sql = "CREATE DATABASE " + database
            csr.execute(sql)

            import time
            time.sleep(1)

            sql = "SHOW DATABASES"
            csr.execute(sql)

            databases = csr.fetchall()

            for db in databases:
                print(db['Database'])
                if database == db:
                    return "Successfully created database " + database
            
            return "Database {} couldn't be created".format(database)

        except Exception as e:
            return "Something went wrong. Probably the database already exists. Error message " + str(e)

    return "Database {} already exists".format(database)


if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
