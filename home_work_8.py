import sqlite3
from sqlite3 import Error

def create_connection(db_name):
    connection = None
    try:
        connection = sqlite3.connect(db_name)
    except Error as e:
        print(e)

    return connection

def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except Error as e:
        print(e)

def insert_countries(connection, country):
    sql = '''INSERT INTO countries
    (title)
    VALUES ('Kyrgyzstan'),('Singapore'),('USA')'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, country)
        connection.commit()
    except Error as e:
        print(e)

def insert_cities(connection, city):
    sql = '''INSERT INTO cities
    (title, area)
    VALUES ('Bishkek', 169),('Chicago', 606),('New York', 1223.3),('Singapore', 734), 
    ('Osh', 182.5), ('Moscow', 2561), ('Los Angeles', 1302)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, city)
        connection.commit()
    except Error as e:
        print(e)

def insert_students(connection, student):
    sql = '''INSERT INTO students
    (first_name, last_name, city_id)
    VALUES ('Bermet', 'Mambetova', 5),('Alinur', 'Kanybekov', 1),('Mark', 'Smith', 3),
    ('Mia', 'Jonson', 7), ('James', 'William', 3), ('Ivan', 'Ivanov', 6), 
    ('Boa', 'Ling', 4),('Lizi', 'James', 2), ('Li', 'Yang', 4), ('Aliza', 'Melisova', 1),
    ('Chen', 'Harper', 4), ('Sveta', 'Petrova', 6), ('Nargiza', 'Kadirova', 5),
    ('Eva','Lim', 2), ('Mina', 'Lucas', 7)'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql, student)
        connection.commit()
    except Error as e:
        print(e)

def select_cities(connection):
    sql = '''SELECT c.id, c.title FROM cities as c'''
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        city_list = cursor.fetchall()

        for city in city_list:
            print(city)
    except Error as e:
        print(e)


create_countries_table = """
CREATE TABLE countries(
    id_country INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL
)
"""
create_cities_table = """
CREATE TABLE cities(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    area FLOAT NOT NULL DEFAULT 0,
    country_id REFERENCES countries(id_country)

)
"""
create_students_table = """
CREATE TABLE students(
    id_student INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    city_id REFERENCES cities(id)
)
"""

join_students_cities = """
SELECT students.first_name, students.last_name,
countries.title, cities.title, cities.area 
FROM students
JOIN cities ON students.city_id = cities.id
JOIN countries ON cities.country_id = countries.id
"""


conn = create_connection('countries.db')
if conn is not None:
    print("Connection sucessful")
    #create_table(conn, create_countries_table)
    #insert_countries(conn, ())
    #create_table(conn, create_cities_table)
    #insert_cities(conn, ())
    #create_table(conn, create_students_table)
    #insert_students(conn, ())
   
conn.close()

city_id = 1

while city_id != 0:
    conn = create_connection('countries.db')
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cities')
        cities_list = cursor.fetchall()
        print("Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
        for city in cities_list:
            print(city)
        city_id = int(input())
        if city_id in [city[0] for city in cities_list]:
            cursor.execute('''
                SELECT students.first_name, students.last_name, countries.title, 
                        cities.title, cities.area
                FROM students
                JOIN cities ON students.city_id = cities.id
                JOIN countries ON cities.country_id = countries.id_country
                WHERE cities.id = ?
            ''', (city_id,))
            students_info = cursor.fetchall()
            for student in students_info:
                print(f'Фамилия: {student[1]}, Имя: {student[0]},  Страна: {student[2]}, Город: {student[3]}, Площадь города: {student[4]}')
        else:
            print("Ввели некорректный id города")
            city_id = int(input())

conn.close()