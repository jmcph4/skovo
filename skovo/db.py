import sqlite3
from . import ts

class TimeSeriesDBInstance(object):
    """
    Representation of a time series in a relational database
    """
    def __init__(self, ts, filename):
        self._ts = ts
        self._filename = filename

        self._db_conn = sqlite3.connect(self._filename)
        self._db_cur = self._db_conn.cursor()

    """
    The underlying time series object
    """
    @property
    def ts(self):
        return self._ts

    """
    The path to the database file
    """
    @property
    def filename(self):
        return self._filename

    def _py2sqlite3_type(self):
        py_type = None
        
        if len(self.ts.data) > 0:
            py_type = type(self.ts.data[list(self.ts.data)[0]])

        if py_type == str:
            return "TEXT"
        elif py_type == int:
            return "INTEGER"
        elif py_type == float:
            return "REAL"
        else:
            return "TEXT"
            
    """
    Writes the time series to the database
    """
    def save(self):
        val_type = self._py2sqlite3_type()

        # create table
        self._db_cur.execute("CREATE TABLE IF NOT EXISTS '{0}' (timestamp TEXT PRIMARY KEY, value {1})".format(self.ts.name, val_type))

        # insert rows
        for k, v in self.ts.data.items():
            self._db_cur.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}')".format(self.ts.name, k, v))

        # commit transaction
        self._db_conn.commit()

    """
    Returns the full SQL code to insert the time series into a database
    """
    def export(self):
        val_type = self._py2sqlite3_type()

        sql = "BEGIN TRANSACTION"
        
        sql += "CREATE TABLE IF NOT EXISTS '{0}' (timestamp TEXT PRIMARY KEY, value {1});".format(self.ts.name, val_type)

        for k, v in self.ts.data.items():
            sql += "INSERT INTO '{0}' VALUES ('{1}', '{2}');".format(self.ts.name, k, v)

        sql += "COMMIT;"

        return sql
