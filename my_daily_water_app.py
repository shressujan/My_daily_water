from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        result = request.form
        # TODO use the information in this reques to store the values  in database
        return redirect('/login')

    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/")
def main():
    return render_template('login.html')


if __name__ == '__main__': app.run()
