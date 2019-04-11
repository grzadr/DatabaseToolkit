import sqlite3 as sql
import pandas as pd
from time import time, localtime, strftime
from IPython.display import display, HTML

def time_log():
    return strftime("%Y-%m-%d %T", localtime(time()))

def log(message, orn=("[", "]")):
    if type(orn) is tuple:
        return "{}{}{} {}".format(orn[0], time_log(), orn[1], message)
    elif type(orn) is str:
        return "{}{}{} {}".format(orn, time_log(), orn, message)
    else:
        return "{} {}".format(orn, time_log(), orn, message)

def init_connection(file_name):
    print(log("### Opening database connection"))

    connection = sql.connect(file_name)
    cursor = connection.cursor()
    cursor.execute("""PRAGMA foreign_keys = ON;""")

    print(log("### Done\n"))

    return connection, cursor


# Terminates connection to database.
# Takes object return by init_connection.
# Returns nothing

def terminate_connection(connection, cursor, clean=False, check=False):
    print(log("### Closing database connection"))

    connection.commit()

    if check:
        cursor.execute("PRAGMA foreign_key_check;")
        cursor.execute("PRAGMA integrity_check;")

    if clean:
        cursor.execute("VACUUM;")
        cursor.execute("PRAGMA optimize;")
    connection.commit()
    connection.close()

    print(log("### Done\n"))

class SQLConnect:
    def __init__(self, file_name: str):
        self.connection, self.cursor = init_connection(file_name)

    def close(self, clean=False):
        terminate_connection(self.connection, self.cursor, clean)

    def execute(self, query: str, *args, kind = "pandas", **kwargs):

        if not len(args):
            result = self.cursor.execute(query).fetchall()
        elif type(args[0]) in (list, tuple):
            result = self.cursor.execute(query, args[0]).fetchall()
        elif len(args) >= 1:
            result = self.cursor.execute(query, args).fetchall()
        else:
            result = self.cursor.execute(query, (args, )).fetchall()

        if kind  == "pandas":
            return pd.DataFrame(result, columns=self.get_columns())
        elif kind == "tuple":
            return (self.get_columns, result )
        else:
            return result if len(result) else None


    def executemany(self, query: str, params):
        return self.cursor.executemany(query, params)

    def get_columns(self):
        return [ele[0] for ele in self.cursor.description]

    def get_tables_names(self):
         return self.cursor.execute(".tables")

def display_info(df : pd.DataFrame, rows = 10,
                 percentiles=[.01, .05, 0.1, .25, .5, .75, .9, .95, .99]):
    if (df is None):
        display("None")
    else:
        if (type(df) is pd.DataFrame):
            display(df.info())
        display(df.describe(percentiles=percentiles))
        display(df.head(rows))
        display(df.tail(rows))

