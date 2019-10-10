from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    states = []
    with open("tmp/states.txt", "r") as ins:
        for line in ins:
            states.append(line)

    if request.method == 'POST':
        result = request.form
        # TODO use the information in this request to store the values  in database
        return redirect('/login')

    return render_template('signup.html', states=states)


@app.route('/input', methods=['POST', 'GET'])
def input_data():
    if request.method == 'POST':
        # TODO validate the form input data and do add to the database
        return redirect('/report')
    return render_template('input.html')


@app.route('/report', methods=['GET'])
def report():
    return render_template('report.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # TODO logic to validate the login info
        return redirect('/input')
    return render_template('login.html')


@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')


@app.route("/")
def main():
    return render_template('login.html')


if __name__ == '__main__': app.run()
