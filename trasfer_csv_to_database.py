import pandas as pd
from my_daily_water_app import add_user, add_daily_water_use
from faker import Faker


def transfer_csv_data_to_database():
    df = pd.read_csv('tmp/water_usage_data.csv')

    emails = df.email
    passwords = df.password
    first_names = df.first_name
    last_names = df.last_name
    street_addresses = df.street
    states = df.state
    cities = df.city
    zip_codes = df.zip
    shower = df.shower
    toilet = df.toilet
    bathroom_sink = df.bathroom_sink
    kitchen_sink = df.kitchen_sink
    drinking_water = df.drinking_water
    sprinkler = df.sprinkler
    miscellaneous = df.miscellaneous

    fake = Faker()

    for i in range(0, len(emails)):
        add_user(emails[i], passwords[i], first_names[i], last_names[i], street_addresses[i], states[i], cities[i],
                 str(zip_codes[i]))
        # TODO To run this function Change the "add_daily_water_use" function in my_daily_water_app to accept date as a input parameter
        add_daily_water_use(emails[i], str(shower[i]), str(toilet[i]), str(bathroom_sink[i]), str(kitchen_sink[i]),
                            str(drinking_water[i]),
                            str(sprinkler[i]), str(miscellaneous[i]), str(fake.date_between()))


def main():
    transfer_csv_data_to_database()


if __name__ == '__main__': main()
