from encryptor import hash_password
import pandas as pd


def generate_hashed_password():
    df = pd.read_csv('tmp/water_usage_data.csv')
    password_column = df.password
    hashed_passwords = []
    for password in password_column:
        hashed_passwords.append(hash_password(str(password)))

    df['hashed_password'] = hashed_passwords
    df.to_csv('tmp/water_usage_data.csv')


def main():
    generate_hashed_password()


if __name__ == '__main__': main()
