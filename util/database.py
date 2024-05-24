from settings import DB
import mysql.connector


class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB['HOST'],
                database=DB['DATABASE'],
                port=DB['PORT'],
                user=DB['USER'],
                password=DB['PASSWORD']
            )
            if self.connection.is_connected():
                print("Successfully connected to database!")
        except mysql.connector.Error:
            self.connection = None
            print("Unable to connect to database!")

    def execute_query(self, query: str, args: tuple = None) -> None:
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, args)
                self.connection.commit()
            except mysql.connector.Error:
                print("Failed to execute query!")

    def fetch_result(self, query: str, args: tuple = None) -> tuple | None:
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, args)
            except mysql.connector.Error:
                print("Failed to fetch result!")
            result = cursor.fetchall()

            cursor.close()

            return result

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Successfully closed database connection!")


# INSTANTIATE DATABASE
db = Database()