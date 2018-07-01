import sys
import csv
import os
from datetime import datetime


def write_to_csv_file(my_dict, output_file):
    fieldnames = ['Name', 'IP Address', 'Response Time', 'Date']

    with open(output_file, 'w') as result:
        writer = csv.DictWriter(result, fieldnames=fieldnames)
        writer.writeheader()
        for index in my_dict:
            writer.writerow({'Name': index,
                             'IP Address': my_dict[index]['ip'],
                             'Response Time': my_dict[index]['ms'],
                             'Date': my_dict[index]['date']})


def get_ping_from_host(reader):
    my_dict = {}

    for row in reader:
        hostname = row['IP Address']
        response = os.popen('ping ' + hostname)
        date = str(datetime.now())[:-7]
        result = str(response.read())
        ip = result.split()[2][1:-1]

        if result.find('ms') == -1:
            my_dict[row['Name']] = {'ip': row['IP Address'],
                                    'ms': 'No Connection',
                                    'date': date}
        else:
            ms = result.split()[-1]
            my_dict[row['Name']] = {'ip': ip,
                                    'ms': ms,
                                    'date': date}
    return my_dict


def get_text_from_database(input_file):
    with open(input_file, 'r') as database:
        reader = list(csv.DictReader(database))
        return reader


def main():
    input_file = None
    output_file = None

    try:
        _, input_file, output_file = sys.argv
    except ValueError:
        pass

    if input_file and output_file is not None:
        write_to_csv_file(get_ping_from_host(get_text_from_database(input_file)), output_file)
    else:
        print('No file has been found')


if __name__ == '__main__':
    main()
