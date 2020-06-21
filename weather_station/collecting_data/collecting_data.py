"""
Used for connecting to the DB and execute different commands
"""

from time import time
import psycopg2
from ..tools.setupparser import SetupParser


class CollectingData:
    """
    CollectingData class is used for connecting to the DB and execute different commands
    """

    def __init__(self):
        self.connect = None
        self._db_connection_params = SetupParser("postgresql").get_param()
        self._db_data_table = SetupParser("db_data_table").get_param()["table"]

    def _db_connection(self):
        """
        Initiate the DB connection
        """
        try:
            print("Connecting to the PostgreSQL database...")
            start_time = time()
            self.connect = psycopg2.connect(**self._db_connection_params)
            print("Connection time: {:.2f} sec".format(time() - start_time))
            print("Database connection successfully")
        except psycopg2.Error as error:
            print("Error while connecting to PostgreSQL", error)

    def _close_connection(self):
        """
        Close the DB connection
        """
        if self.connect:
            self.connect.close()
            print("Database connection closed.")

    def _db_checkup(self):
        """
        Validate the DB structure
        """
        self.validate_table(self._db_data_table)

    def execute_psql_command(self, command, save=True):
        """
        Execute CRUD commands
        :param command:
            CRUD command
        :param save:
            Used to know if the changed done in db should be saved
        :raise:
            Raise exception if the CRUD command was not executed
        """
        self._db_connection()
        cursor = self.connect.cursor()
        try:
            cursor.execute(command)
        except (Exception, psycopg2.Error) as error:
            print(error)
            self._close_connection()
            raise
        if save:
            self.connect.commit()
        self._close_connection()

    def validate_table(self, table):
        """
        Check if the table is available in the db
        :param table:
            Table that need to be checked in the db
        :raise:
            Raise exception if the tabel is not in the db
        """
        print("Check if {} table is available in the database ...".format(table))
        try:
            self.execute_psql_command('''SELECT * FROM {};'''.format(table), False)
        except psycopg2.Error:
            if table == self._db_data_table:
                print("{} table is missing from database".format(table))
                self.table_creation(table)

    def table_creation(self, table):
        """
        Creates the table in the db
        :param table:
            Table that need to be created in the db
        """
        print("Generating {} table ...".format(table))
        self.execute_psql_command('''CREATE TABLE {}
                                    (date DATE PRIMARY KEY NOT NULL,
                                    speed REAL NOT NULL,
                                    direction_degrees REAL NOT NULL,
                                    direction_voltage REAL NOT NULL,
                                    direction CHAR(4) NOT NULL,
                                    rain_qty REAL NOT NULL);'''.format(table))
        print("weather_data table created")

    def insert_data(self, values):
        print("Inserting new values ...")
        # self.execute_psql_command('''INSERT INTO {} (date, speed, direction_degrees, direction_voltage, direction,
        # rain_qty) VALUES {}''' % (self._db_data_table,values))
        print('''INSERT INTO {} (date, speed, direction_degrees, direction_voltage, direction, 
        rain_qty) VALUES {}''' % (self._db_data_table,values))


if __name__ == '__main__':
    DB = CollectingData()
