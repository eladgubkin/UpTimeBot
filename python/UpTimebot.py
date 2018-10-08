import csv
import os
import socket
from datetime import datetime
import requests


class Service(object):
    def __init__(self, row, complete_dict):
        self.row = row
        self.complete_dict = complete_dict

    def ping(self):
        response = os.popen('ping ' + self.row['IP Address'])
        date = str(datetime.now())[:-7]
        result = str(response.read())
        ip = socket.gethostbyname(self.row['IP Address'])

        if result.find('ms') == -1:
            self.complete_dict[self.row['Name']] = {'ip': ip,
                                                    'response': 'ping: No Connection',
                                                    'date': date}
        else:
            ms = 'ping: ' + result.split()[-1]
            self.complete_dict[self.row['Name']] = {'ip': ip,
                                                    'response': ms,
                                                    'date': date}
        return self.complete_dict

    def traceroute(self):
        response = os.popen('tracert ' + self.row['IP Address'])
        date = str(datetime.now())[:-7]
        hops = 'traceroute: ' + str(len(response.readlines()) - 6) + ' hops'
        ip = socket.gethostbyname(self.row['IP Address'])

        self.complete_dict[self.row['Name']] = {'ip': ip,
                                                'response': hops,
                                                'date': date}
        return self.complete_dict

    def get_http(self):
        req = requests.get(r'http://' + self.row['IP Address'])
        date = str(datetime.now())[:-7]
        ip = socket.gethostbyname(self.row['IP Address'])
        response = 'HTTP GET: ' + str(req.status_code)

        self.complete_dict[self.row['Name']] = {'ip': ip,
                                                'response': response,
                                                'date': date}
        return self.complete_dict


def write_to_csv_file(complete_dict, output_file):
    fieldnames = ['Name', 'IP Address', 'Response', 'Date']

    with open(output_file, 'w') as result:
        writer = csv.DictWriter(result, fieldnames=fieldnames)
        writer.writeheader()
        for index in complete_dict:
            writer.writerow({'Name': index,
                             'IP Address': complete_dict[index]['ip'],
                             'Response': complete_dict[index]['response'],
                             'Date': complete_dict[index]['date']})


def define_service(reader, complete_dict):
    for row in reader:
        service = Service(row, complete_dict)
        if row['Service'] == 'ping':
            service.ping()

        elif row['Service'] == 'traceroute':
            service.traceroute()

        elif row['Service'].lower() == 'get':
            service.get_http()

        else:
            print(row['Service'] + ' is not a Service.')

    return complete_dict


def get_text_from_database(input_file):
    with open(input_file, 'r') as database:
        reader = list(csv.DictReader(database))
        return reader


def main():
    input_file = "../csv/database.csv"
    output_file = "../csv/result.csv"
    complete_dict = {}

    if input_file and output_file is not None:
        write_to_csv_file(
            define_service(
                get_text_from_database(
                    input_file), complete_dict), output_file)

    else:
        print('No file has been found')


if __name__ == '__main__':
    main()
