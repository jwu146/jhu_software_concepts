"""Module for loading applicant data into a PostgreSQL database."""

import json
import argparse
from pathlib import Path
import psycopg2
from psycopg2 import OperationalError

INSERT_QUERY = """
    INSERT INTO applicants (
        p_id, program, university, comments, date_added, url, status, date_decision, term,
        us_or_international, gpa, gre, gre_v, gre_aw, degree
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (p_id) DO UPDATE SET
        program = EXCLUDED.program,
        university = EXCLUDED.university,
        comments = EXCLUDED.comments,
        date_added = EXCLUDED.date_added,
        url = EXCLUDED.url,
        status = EXCLUDED.status,
        date_decision = EXCLUDED.date_decision,
        term = EXCLUDED.term,
        us_or_international = EXCLUDED.us_or_international,
        gpa = EXCLUDED.gpa,
        gre = EXCLUDED.gre,
        gre_v = EXCLUDED.gre_v,
        gre_aw = EXCLUDED.gre_aw,
        degree = EXCLUDED.degree
;
"""

def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Creates a connection to a PostgreSQL database.

    Args:
        db_name (str): Name of the database.
        db_user (str): Username for authentication.
        db_password (str): Password for authentication.
        db_host (str): Hostname or IP address of the database server.
        db_port (str or int): Port number of the database server.

    Returns:
        connection: psycopg2 connection object if successful, else None.
    """
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"Error while connecting to database:\n{e}")
    return connection

def create_table(connection):
    """Drops the applicants table if it exists and creates a new applicants table.

    Args:
        connection: psycopg2 database connection object.

    Returns:
        None
    """
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS applicants;")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS applicants (
        p_id INTEGER PRIMARY KEY,
        program TEXT,
        university TEXT,
        comments TEXT,
        date_added DATE,
        url TEXT,
        status TEXT,
        date_decision TEXT,
        term TEXT,
        us_or_international TEXT,
        gre FLOAT,
        gre_v FLOAT,
        degree TEXT,
        gpa FLOAT,
        gre_aw FLOAT
    );
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table checked/created successfully.")
    except OperationalError as e:
        print(f"Error while creating table:\n{e}")
    cursor.close()

def insert_data(connection, data):
    """Inserts applicant data into the applicants table.

    Args:
        connection: psycopg2 database connection object.
        data (list): List of dictionaries containing applicant data.

    Returns:
        None
    """
    cursor = connection.cursor()
    for i, applicant in enumerate(data):
        cursor.execute(INSERT_QUERY, (
            i,
            applicant.get('program'),
            applicant.get('university'),
            applicant.get('comments'),
            applicant.get('date_added'),
            applicant.get('url'),
            applicant.get('status'),
            applicant.get('date_decision'),
            applicant.get('term'),
            applicant.get('nationality'),
            applicant.get('gpa'),
            applicant.get('gre'),
            applicant.get('gre_v'),
            applicant.get('gre_aw'),
            applicant.get('degree')
        ))
    connection.commit()
    print("Data inserted successfully.")
    cursor.close()

def parse_args():
    """Parses command-line arguments for database credentials.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Load applicant data into PostgreSQL.")
    parser.add_argument('--db_name', default='postgres', help='Database name')
    parser.add_argument('--db_user', default='postgres', help='Database user')
    parser.add_argument('--db_password', default='12345', help='Database password')
    parser.add_argument('--db_host', default='localhost', help='Database host')
    parser.add_argument('--db_port', default='5432', help='Database port')
    return parser.parse_args()

def main(cmd_args):
    """Main entry point for loading data.

    Args:
        cmd_args: Parsed command-line arguments.

    Returns:
        None
    """
    conn = create_connection(
        db_name=cmd_args.db_name,
        db_user=cmd_args.db_user,
        db_password=cmd_args.db_password,
        db_host=cmd_args.db_host,
        db_port=cmd_args.db_port
    )
    if conn is None:
        print("Failed to connect to DB. Exiting.")
        return

    create_table(conn)

    data_path = Path(__file__).parent / "data" / "applicant_data.json"
    with open(data_path, 'r', encoding='utf-8') as file:
        applicants = json.load(file)
    insert_data(conn, applicants)

    conn.close()

if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
