import sqlite3

connection = sqlite3.connect('phonebook.db')
cursor = connection.cursor()


def contact_list():
    cursor.execute("select * from phonebook")
    return cursor.fetchall()


def add_contact(lst):
    cursor.execute("insert into phonebook"
                   "(last_name, name, phone)"
                   "values (?, ?, ?);", lst)
    connection.commit()
