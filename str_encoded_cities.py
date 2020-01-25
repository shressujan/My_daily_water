import random


def main():
    encoded_cities = open("tmp/encodedCitiesList.txt", "w+")

    file = open("tmp/cities.txt", "r")
    lines = file.readlines()
    for line in lines:
        temp = line.strip("\n")
        encoded_cities.write("'" + temp + "',")

    encoded_cities.close()
    file.close()


def output_random_city():
    file = open("tmp/cities.txt", "r")
    lines = file.readlines()
    random_city = lines[(random.randint(0, len(lines) - 1))].strip('\n')

    file.close()
    return random_city


if __name__ == '__main__': main()
