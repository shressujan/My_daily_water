from flask import Flask, render_template

my_daily_water_app = Flask(__name__)


@my_daily_water_app.route("/")
def main():
    return render_template('index.html')


if __name__ == '__main__': my_daily_water_app.run()
