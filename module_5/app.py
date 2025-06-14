"""Flask web application for displaying PostgreSQL query results."""

import argparse
from flask import Flask, render_template
import psycopg2
import query_data

app = Flask(__name__)
ARGS = None
LIMIT = 100

def get_db_connection(db_args):
    """Handles database connection.

    Args:
        db_args: Parsed command-line arguments with DB credentials.

    Returns:
        psycopg2 connection object.
    """
    db_config = {
        'dbname': db_args.db_name,
        'user': db_args.db_user,
        'password': db_args.db_password,
        'host': db_args.db_host,
        'port': db_args.db_port
    }
    return psycopg2.connect(**db_config)

@app.route("/")
def home():
    """Main route for displaying results page."""
    conn = query_data.create_connection(
        ARGS.db_name, ARGS.db_user, ARGS.db_password, ARGS.db_host, ARGS.db_port
    )
    if conn is None:
        return "Database connection failed."
    results = {
        "spring_2025_count": query_data.count_spring_2025_entries(conn),
        "percent_international": query_data.percent_international(conn),
        "avg_gpa": f"{query_data.average_metrics(conn)[0]:.2f}",
        "avg_gre": f"{query_data.average_metrics(conn)[1]:.2f}",
        "avg_gre_v": f"{query_data.average_metrics(conn)[2]:.2f}",
        "avg_gre_aw": f"{query_data.average_metrics(conn)[3]:.2f}",
        "avg_gpa_american": f"{query_data.average_gpa_american_spring_2025(conn):.2f}",
        "percent_accept_spring": query_data.percent_acceptances_spring_2025(conn),
        "avg_gpa_accepted": f"{query_data.average_gpa_accepted_spring_2025(conn):.2f}",
        "jhu_cs_masters": query_data.count_jhu_cs_masters(conn),
    }
    conn.close()
    return render_template("results.html", **results)

def parse_args():
    """Parses command-line arguments for DB connection.

    Returns:
        Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Query applicant data from PostgreSQL.")
    parser.add_argument('--db_name', default='postgres', help='Database name')
    parser.add_argument('--db_user', default='postgres', help='Database user')
    parser.add_argument('--db_password', default='12345', help='Database password')
    parser.add_argument('--db_host', default='localhost', help='Database host')
    parser.add_argument('--db_port', default='5432', help='Database port')
    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_args()
    app.run(debug=True)
