from flask import Flask, render_template, request, redirect, json, url_for, session
from flaskext.mysql import MySQL
from datetime import date
from encryptor import *

app = Flask(__name__)
app.secret_key = 'password'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ROOT321$'
app.config['MYSQL_DATABASE_DB'] = 'Daily_water_tracker'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)


def add_user(email, password, first_name, last_name, street_address, state, city, zip_code):
    db_connection = mysql.connect()
    cursor = db_connection.cursor()
    cursor.callproc('sp_add_user',
                    (email, hash_password(password), first_name, last_name, street_address, state, city, zip_code))
    data = cursor.fetchall()

    if len(data) is 0:
        db_connection.commit()
        return json.dumps({'message': 'User created successfully !'})
    else:
        return json.dumps({'error': str(data[0])})


def get_saved_daily_water_use_data(username):
    get_saved_data_sql_query = "SELECT * FROM Daily_Water_Usage WHERE username = %s AND date = %s"
    saved_user_data = (username, date.today())

    db_connection = mysql.connect()
    cursor = db_connection.cursor()
    cursor.execute(get_saved_data_sql_query, saved_user_data)
    result = cursor.fetchone()

    cursor.close()
    return result


def save_daily_water_use(username, shower, toilet, bathroom_sink, kitchen_sink, drinking_water,
                         sprinkler, miscellaneous):
    db_connection = mysql.connect()
    cursor = db_connection.cursor()
    cursor.callproc('sp_add_daily_water_data',
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
        # TODO return a message to user saying user name doesn't exist instead of just returning 0
        return 0


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

        if email == '' or password == '' or first_name == '' or last_name == '' or street_address == '' or city == '' or state == '' or zip_code == '':
            return json.dumps({'error': 'missing fields!! Try Again'})
        add_user(email, password, first_name, last_name, street_address, state, city, zip_code)

        return redirect(url_for('login', user_email=email, user_password=password))

    return render_template('signup.html')


# @app.route('/input', defaults={'user_email': None}, methods=['POST'])
@app.route('/input/<user_email>', methods=['GET', 'POST'])
def input_data(user_email):
    # validates that the user trying to input is logged in
    if 'username' in session:
        username = session['username']
        if username != user_email:
            return json.dumps({'error': 'User ' + username + 'is not logged in!'})
    else:
        return json.dumps({'error': 'User ' + user_email + 'is not logged in!'})

    # If POST request is made
    if request.method == 'POST':
        shower = request.form['shower_input']
        kitchen_sink = request.form['kitchen_sink_input']
        bathroom_sink = request.form['bathroom_sink_input']
        toilet = request.form['toilet_input']
        drinking_water_input = request.form['drinking_water_input']
        sprinkler = request.form['sprinkler_input']
        miscellaneous = request.form['miscellaneous_input']

        save_daily_water_use(user_email, shower, toilet, bathroom_sink, kitchen_sink, drinking_water_input,
                             sprinkler, miscellaneous)

        return redirect(url_for('report', username=user_email))

    # Gets the saved water data for the current date
    saved_data = get_saved_daily_water_use_data(user_email)

    if saved_data:
        shower = saved_data[1]
        kitchen_sink = saved_data[2]
        bathroom_sink = saved_data[3]
        toilet = saved_data[4]
        drinking_water_input = saved_data[5]
        sprinkler = saved_data[6]
        miscellaneous = saved_data[7]
    else:
        shower = 0
        kitchen_sink = 0
        bathroom_sink = 0
        toilet = 0
        drinking_water_input = 0
        sprinkler = 0
        miscellaneous = 0

    # render input page with given values for the input
    return render_template('input.html', username=user_email, shower_saved_data=shower,
                           kitchen_sink_saved_data=kitchen_sink,
                           bathroom_sink_saved_data=bathroom_sink, toilet_saved_data=toilet,
                           drinking_water_saved_data=drinking_water_input, sprinkler_saved_data=sprinkler,
                           miscellaneous_saved_data=miscellaneous)


@app.route('/report/<username>')
def report(username):
    # TODO render the report template for the given user
    get_water_usage_date_query = "SELECT * FROM Daily_Water_Usage where username = %s"
    username_data = (username,)

    db_connection = mysql.connect()
    cursor = db_connection.cursor()
    cursor.execute(get_water_usage_date_query, username_data)
    result = cursor.fetchall()

    if result:
        # TODO show the result in graph form
        print('how to show the result in graph')
        return render_template('report.html')
    else:
        return json.dumps({'error': 'No record entry found for User ' + username})
    return None


@app.route('/login', defaults={'user_email': '', 'user_password': ''}, methods=['GET', 'POST'])
@app.route('/login/<user_email>/<user_password>', methods=['GET', 'POST'])
def login(user_email, user_password):

    # checks if user is already logged in, opens up the input page for that user
    if 'username' in session:
        username = session['username']
        return redirect(url_for('input_data', user_email=username))

    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']

        if email == '' or password == '':
            return json.dumps({'error': 'Please Enter Username and password!!'})

        if is_valid_login(email, password):
            session['username'] = email
            return redirect(url_for('input_data', user_email=email))
        else:
            return json.dumps({'error': 'Login Failed!!'})
    elif user_email == '' and user_password == '':
        return render_template('login.html')

    return render_template('login.html', user_email=user_email, user_password=user_password)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        return render_template('login.html')
    else:
        return json.dumps({'error': 'User has already Logged out'})


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def index():
    return render_template('about.html')


if __name__ == '__main__': app.run()
