import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):

    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"C:\\sqlite\db\\remindme.db"

    sql_create_remindme_table = """ CREATE TABLE IF NOT EXISTS reminders (
                                        id INTEGER PRIMARY KEY,
                                        userID TEXT NOT NULL,
                                        timeGenerated BIGINT NOT NULL,
                                        timeToRemind BIGINT NOT NULL,
                                        channelID TEXT NOT NULL,
                                        postID TEXT NOT NULL,
                                        username text NOT NULL,
                                        triggerWord TEXT NOT NULL,
                                        teamDomain TEXT NOT NULL,
                                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        print("creating tables")
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
