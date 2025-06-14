"""Module for querying applicant data from a PostgreSQL database."""

import argparse
import psycopg2
from psycopg2 import sql

LIMIT = 100

def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Creates a connection to a PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
        return connection
    except psycopg2.OperationalError as error:
        print(f"Database connection failed: {error}")
        return None

def count_spring_2025_entries(connection):
    """Counts number of applicants for Spring 2025."""
    cursor = connection.cursor()
    query = sql.SQL(
        "SELECT COUNT(*) FROM {table} WHERE {col} ILIKE {pattern} LIMIT {limit}"
    ).format(
        table=sql.Identifier('applicants'),
        col=sql.Identifier('term'),
        pattern=sql.Literal('%Spring 2025%'),
        limit=sql.Literal(LIMIT),
    )
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result

def percent_international(connection):
    """Calculates percentage of international students (not American or Other)."""
    cursor = connection.cursor()
    # International count
    query_intl = sql.SQL(
        "SELECT COUNT(*) FROM {table} WHERE {col} ILIKE {pattern} LIMIT {limit}"
    ).format(
        table=sql.Identifier('applicants'),
        col=sql.Identifier('us_or_international'),
        pattern=sql.Literal('%International%'),
        limit=sql.Literal(LIMIT),
    )
    cursor.execute(query_intl)
    international = cursor.fetchone()[0]
    # Total count
    query_total = sql.SQL(
        "SELECT COUNT(*) FROM {table} LIMIT {limit}"
    ).format(
        table=sql.Identifier('applicants'),
        limit=sql.Literal(LIMIT),
    )
    cursor.execute(query_total)
    total = cursor.fetchone()[0]
    percent = (international / total) * 100 if total > 0 else 0
    cursor.close()
    return round(percent, 2)

def average_metrics(connection):
    """Finds the average GPA, GRE, GRE V, and GRE AW for applicants who provided each metric."""
    cursor = connection.cursor()
    metrics = {}
    for col in ['gpa', 'gre', 'gre_v', 'gre_aw']:
        query = sql.SQL(
            "SELECT AVG({col}) FROM {table} WHERE {col} IS NOT NULL LIMIT {limit}"
        ).format(
            col=sql.Identifier(col),
            table=sql.Identifier('applicants'),
            limit=sql.Literal(LIMIT),
        )
        cursor.execute(query)
        metrics[col] = cursor.fetchone()[0]
    cursor.close()
    return metrics['gpa'], metrics['gre'], metrics['gre_v'], metrics['gre_aw']

def average_gpa_american_spring_2025(connection):
    """Finds average GPA of American students who applied for Spring 2025."""
    cursor = connection.cursor()
    query = sql.SQL("""
        SELECT AVG({gpa}) FROM {table}
        WHERE {nation} ILIKE {american}
        AND {term_col} ILIKE {term}
        AND {gpa} IS NOT NULL
        LIMIT {limit}
    """).format(
        gpa=sql.Identifier('gpa'),
        table=sql.Identifier('applicants'),
        nation=sql.Identifier('us_or_international'),
        american=sql.Literal('%American%'),
        term_col=sql.Identifier('term'),
        term=sql.Literal('%Spring 2025%'),
        limit=sql.Literal(LIMIT),
    )
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result

def percent_acceptances_spring_2025(connection):
    """Percent of Spring 2025 entries that are Acceptances."""
    cursor = connection.cursor()
    # Total
    query_total = sql.SQL(
        "SELECT COUNT(*) FROM {table} WHERE {term_col} ILIKE {term} LIMIT {limit}"
    ).format(
        table=sql.Identifier('applicants'),
        term_col=sql.Identifier('term'),
        term=sql.Literal('%Spring 2025%'),
        limit=sql.Literal(LIMIT),
    )
    cursor.execute(query_total)
    total = cursor.fetchone()[0]
    # Accepted
    query_accepted = sql.SQL("""
        SELECT COUNT(*) FROM {table}
        WHERE {term_col} ILIKE {term}
        AND {status_col} ILIKE {status}
        LIMIT {limit}
    """).format(
        table=sql.Identifier('applicants'),
        term_col=sql.Identifier('term'),
        term=sql.Literal('%Spring 2025%'),
        status_col=sql.Identifier('status'),
        status=sql.Literal('%Accepted%'),
        limit=sql.Literal(LIMIT),
    )
    cursor.execute(query_accepted)
    accepted = cursor.fetchone()[0]
    percent = (accepted / total) * 100 if total > 0 else 0
    cursor.close()
    return round(percent, 2)

def average_gpa_accepted_spring_2025(connection):
    """Average GPA of accepted applicants who applied for Spring 2025."""
    cursor = connection.cursor()
    query = sql.SQL("""
        SELECT AVG({gpa}) FROM {table}
        WHERE {term_col} ILIKE {term}
        AND {status_col} ILIKE {status}
        AND {gpa} IS NOT NULL
        LIMIT {limit}
    """).format(
        gpa=sql.Identifier('gpa'),
        table=sql.Identifier('applicants'),
        term_col=sql.Identifier('term'),
        term=sql.Literal('%Spring 2025%'),
        status_col=sql.Identifier('status'),
        status=sql.Literal('%Accepted%'),
        limit=sql.Literal(LIMIT),
    )
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result

def count_jhu_cs_masters(connection):
    """Counts entries for JHU, masters, Computer Science."""
    cursor = connection.cursor()
    jhu_conditions = [
        sql.SQL("{univ} ILIKE {val}").format(
            univ=sql.Identifier('university'),
            val=sql.Literal(pattern)
        ) for pattern in [
            '%JHU%', '%Johns Hopkins%', '%John Hopkins%', '%John Hopkin%', '%Johns Hopkin%'
        ]
    ]
    degree_conditions = [
        sql.SQL("{deg} ILIKE {val}").format(
            deg=sql.Identifier('degree'),
            val=sql.Literal(pattern)
        ) for pattern in [
            '%Master%', '%MS%', '%Masters%'
        ]
    ]
    where_clause = (
        sql.SQL("(")
        + sql.SQL(" OR ").join(jhu_conditions)
        + sql.SQL(") AND (")
        + sql.SQL(" OR ").join(degree_conditions)
        + sql.SQL(")")
    )
    query = sql.SQL("""
        SELECT COUNT(*) FROM {table}
        WHERE {where_clause}
        AND {prog} ILIKE {cs}
        LIMIT {limit}
    """).format(
        table=sql.Identifier('applicants'),
        where_clause=where_clause,
        prog=sql.Identifier('program'),
        cs=sql.Literal('%Computer Science%'),
        limit=sql.Literal(LIMIT),
    )
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result

def parse_args():
    """Parses command-line arguments for DB connection.

    Returns:
        Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Query applicant data from PostgreSQL.")
    parser.add_argument('--db_name', default='postgres', help='Database name')
    parser.add_argument('--db_user', default='postgres', help='Database user')
    parser.add_argument('--db_password', default='12345', help='Database password')
    parser.add_argument('--db_host', default='localhost', help='Database host')
    parser.add_argument('--db_port', default='5432', help='Database port')
    return parser.parse_args()

def main():
    """Main function to parse arguments and run queries."""
    args = parse_args()
    db_conn = create_connection(
        db_name=args.db_name,
        db_user=args.db_user,
        db_password=args.db_password,
        db_host=args.db_host,
        db_port=args.db_port
    )
    if db_conn:
        print(f"Entries for Spring 2025: {count_spring_2025_entries(db_conn)}")
        print(f"Percentage of international students: {percent_international(db_conn)}")
        metrics = average_metrics(db_conn)
        print(f"Average GPA: {metrics[0]:.2f}, "
              f"GRE: {metrics[1]:.2f}, "
              f"GRE V: {metrics[2]:.2f}, "
              f"GRE AW: {metrics[3]:.2f} ")
        print(f"Average GPA (American, Spring 2025): "
              f"{average_gpa_american_spring_2025(db_conn):.2f}")
        print(f"Percent Acceptances (Spring 2025): {percent_acceptances_spring_2025(db_conn):.2f}")
        print(f"Average GPA (Accepted, Spring 2025): "
              f"{average_gpa_accepted_spring_2025(db_conn):.2f}")
        print(f"JHU Masters Computer Science applicants: {count_jhu_cs_masters(db_conn)}")
        db_conn.close()

if __name__ == "__main__":
    main()
