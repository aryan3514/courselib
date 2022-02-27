import psycopg2
from psycopg2 import Error

def start_db():
      # Connect to an existing database
      connection = psycopg2.connect(user="postgres",
                                    password="IZumbVFIcn",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="postgres")
      # Print PostgreSQL details
      print("PostgreSQL server information")
      print(connection.get_dsn_parameters(), "\n")
      return connection