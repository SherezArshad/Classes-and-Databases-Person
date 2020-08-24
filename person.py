import re, os , unittest
import sqlite3
import sys



class Person:

    def __init__(self, first = '', last = '', birthday = '' , email = ''):
        self.first = first
        self.last = last
        self.bday = birthday
        self.email = email

        if self.first == '':
            self.first = input("Enter person's first name: ")
        if self.last == '':
            self.last = input("Enter person's last name: ")
        if self.bday == '':
            self.bday = input("Enter person's birthday: ")
        if self.email == '':
            self.email = input("Enter person's e-mail: ")



    def __repr__(self):
        return str(self.first + " " + self.last+ ": " + self.bday + ", " + self.email)


    @classmethod
    def read_person(cls, file):

        first = file.readline().strip()
        if not first:
            return False
        last = file.readline().strip()
        bday = file.readline().strip()
        email = file.readline().strip()
        return cls(first, last, bday, email)


    def write_person(self, file):
        file.write(self.first + '\n' + self.last + '\n' + self.bday + '\n' + self.email + '\n')



def open_persons_db():
    exists = os.path.exists('persons.db')
    persons_db = sqlite3.connect('persons.db')
    persons_db.row_factory = sqlite3.Row

    if exists == False:
        persons_db.execute('CREATE TABLE friends (first TEXT, last TEXT, bday TEXT, email TEXT PRIMARY KEY)')
        persons_db.execute('CREATE TABLE colleagues (first TEXT, last TEXT, bday TEXT, email TEXT PRIMARY KEY)')
        persons_db.commit()
    return persons_db


def add_person(person_database, person_object,  friend = True, colleague = False):



    if friend == False and colleague == False:
        print('Warning: ' + person_object.email + ' not added - must be friend or colleague', file = sys.stderr)
        return False
    if friend:
        person_database.execute('INSERT INTO friends (first, last, bday, email) VALUES (?,?,?,?);',(person_object.first, person_object.last, person_object.bday, person_object.email))

    if colleague:
        person_database.execute('INSERT INTO colleagues (first, last, bday, email) VALUES (?,?,?,?);',(person_object.first, person_object.last, person_object.bday, person_object.email))

    return True

    person_database.commit()

def delete_person(Person_database, Person):
    Person_database.execute('DELETE FROM friends WHERE email = ?;',(Person.email,))
    Person_database.execute('DELETE FROM colleagues WHERE email = ?;',(Person.email,))






def to_Person_list(cursor):



    lst = []
    rows = cursor.fetchall()

    for row in rows:
        first = row['first']
        last = row['last']
        bday = row['bday']
        email = row['email']

        lst.append(Person(first, last, bday, email))



    return lst


def get_friends(Person_database):

    return to_Person_list(Person_database.execute('SELECT * FROM friends;'))



def get_colleagues(colleagues_database):

    return to_Person_list(colleagues_database.execute('SELECT * FROM colleagues;'))



'''
is exactly the same as get_friends. Only difference is that
#The query is retrieving information from a different table
'''

def get_all(person_database):
    return to_Person_list(person_database.execute('SELECT * FROM friends UNION SELECT * FROM colleagues;'))




def get_and(person_database):

    return to_Person_list(person_database.execute('SELECT DISTINCT * FROM friends AS F JOIN colleagues AS c ON f.email == c.email;'))
