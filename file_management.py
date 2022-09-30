import csv
import database


def write_in_txt(file_name, lst):
    with open(file_name, 'w') as f:
        [f.write(' '.join(item) + '\n') for item in lst]


def write_in_csv(file_name, lst):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(lst)


def file_read_txt(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        [database.add_contact(item.split()) for item in f.readlines()]


def file_read_csv(file_name):
    with open(file_name, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f, delimiter=';'))
    [database.add_contact(item) for item in reader]
