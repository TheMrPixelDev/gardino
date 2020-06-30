import sqlite3

class database():

    def __init__(self, database):
        self.database_name = database

    def read(self, table,columns):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(f"SELECT {columns} FROM {table}")
        data_list = cursor.fetchall()
        return data_list

    def read_one(self, table,columns):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(f"SELECT {columns} FROM {table}")
        data_list = cursor.fetchone()
        return data_list

    #This function reads from a database by a certain condition
    def read_conditional(self, columns, condition):

        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(f"SELECT {columns} FROM weather_data WHERE {condition} ORDER BY time DESC")
        data_list = cursor.fetchall()

        return data_list

    def write(self, table, columns, data):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        placehoder_list = []
        separator = ','
        for _ in data:
            placehoder_list.append('?')
        placehoder_string = separator.join(placehoder_list)
        cursor.execute(f'INSERT INTO {table} ({columns}) VALUES ({placehoder_string})', data)
        connection.commit()
        connection.close()


