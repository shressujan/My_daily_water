from flask import Flask, render_template, request, redirect, json, url_for
from flaskext.mysql import MySQL
from datetime import date
from encryptor import *

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Water_Usage_Tracker'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['signupInputEmail']
        password = request.form['signupInputPassword']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        street_address = request.form['inputAddress']
        city = request.form['inputCity']
        state = request.form['inputState']
        zip_code = request.form['inputZip']

        add_user(email, password, first_name, last_name, street_address, state, city, zip_code)

        return redirect(url_for('login', user_email=email, user_password=password))

    return render_template('signup.html')


@app.route('/input/<user_email>', methods=['GET', 'POST'])
def input_data(user_email):

    if request.method == 'POST':
        shower = request.form['shower_input']
        kitchen_sink = request.form['kitchen_sink_input']
        bathroom_sink = request.form['bathroom_sink_input']
        toilet = request.form['toilet_input']
        drinking_water_input = request.form['drinking_water_input']
        sprinkler = request.form['garden_hose_input']
        miscellaneous = request.form['miscellaneous_input']

        add_daily_water_use(user_email, shower, toilet, bathroom_sink, kitchen_sink, drinking_water_input,
                            sprinkler, miscellaneous)

        return redirect(url_for('report', user_email=user_email))

    return render_template('input.html')


@app.route('/report/<user_email>')
def report(user_email):
    # TODO render the report template for the given user
    return render_template('report.html')


@app.route('/login', defaults={'user_email': '', 'user_password': ''}, methods=['GET', 'POST'])
@app.route('/login/<user_email>/<user_password>', methods=['GET', 'POST'])
def login(user_email, user_password):
    if user_email == '' and user_password == '':
        redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        if is_valid_login(email, password):
            return redirect(url_for('input_data', user_email=email))
        else:
            print('do something here')

    return render_template('login.html', user_email=user_email, user_password=user_password)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def index():
    return render_template('login.html')


if __name__ == '__main__': app.run()


def add_user(email, password, first_name, last_name, street_address, state, city, zip_code):
    db_connection = mysql.connect()
    cursor = db_connection.cursor()
    cursor.callproc('sp_createUser',
                    (email, hash_password(password), first_name, last_name, street_address, state, city, zip_code))
    data = cursor.fetchall()

    if len(data) is 0:
        db_connection.commit()
        return json.dumps({'message': 'User created successfully !'})
    else:
        return json.dumps({'error': str(data[0])})


def add_daily_water_use(username, shower, toilet, bathroom_sink, kitchen_sink, drinking_water,
                        sprinkler, miscellaneous):
    db_connection = mysql.connect()
    cursor = db_connection.cursor()
    cursor.callproc('sp_add_daily_water_usage_data',
                    (username, shower, toilet, bathroom_sink, kitchen_sink, drinking_water,
                     sprinkler, miscellaneous, date.today()))
    data = cursor.fetchall()

    if len(data) is 0:
        db_connection.commit()
        cursor.close()
        return json.dumps({'message': 'Daily Water Use data added successfully !'})
    else:
        cursor.close()
        return json.dumps({'error': str(data[0])})


def is_valid_login(username, user_password):

    get_user_account_sql_query = "SELECT * FROM User_Account WHERE username = %s"
    username_data = (username,)

    db_connection = mysql.connect()
    cursor = db_connection.cursor()
    cursor.execute(get_user_account_sql_query, username_data)
    result = cursor.fetchone()

    if result:
        return check_password_matches(result[1], user_password)
    else:
        # TODO return a message to user saying user name doesn't exist
        print("User account does not exist!")
