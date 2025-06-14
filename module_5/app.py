"""Flask web application for displaying PostgreSQL query results."""

import argparse
from flask import Flask, render_template
import psycopg2

app = Flask(__name__)
ARGS = None

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

def get_results(db_args):
    """Handles queries from database and returns a dictionary with results.

    Args:
        db_args: Parsed command-line arguments with DB credentials.

    Returns:
        dict: Results of queries formatted for display.
    """
    conn = get_db_connection(db_args)
    cur = conn.cursor()

    # Query 1: Entries for Spring 2025
    cur.execute(
        "SELECT COUNT(*) FROM applicants WHERE term ILIKE '%Spring 2025%'")
    spring_2025_count = cur.fetchone()[0]

    # Query 2: Percent international students
    cur.execute(
        "SELECT COUNT(*) FROM applicants WHERE us_or_international ILIKE '%International%'")
    international = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM applicants")
    total = cur.fetchone()[0]
    percent_international = (international / total * 100) if total else 0

    # Query 3: Average GPA, GRE, GRE V, GRE AW (each individually)
    def get_avg(col):
        cur.execute(
            f"SELECT AVG({col}) FROM applicants WHERE {col} IS NOT NULL")
        return cur.fetchone()[0]

    avgs = {
        "gpa": get_avg("gpa"),
        "gre": get_avg("gre"),
        "gre_v": get_avg("gre_v"),
        "gre_aw": get_avg("gre_aw"),
    }

    # Query 4: Average GPA of American students in Spring 2025
    cur.execute("""
        SELECT AVG(gpa) FROM applicants
        WHERE us_or_international ILIKE '%American%'
        AND term ILIKE '%Spring 2025%'
        AND gpa IS NOT NULL
    """)
    avg_gpa_american = cur.fetchone()[0]

    # Query 5: % Acceptances Spring 2025
    cur.execute(
        "SELECT COUNT(*) FROM applicants WHERE term ILIKE '%Spring 2025%'")
    total_spring = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(*) FROM applicants
        WHERE term ILIKE '%Spring 2025%' AND status ILIKE '%Accepted%'
    """)
    accepted_spring = cur.fetchone()[0]
    percent_accept_spring = (accepted_spring / total_spring * 100) if total_spring else 0

    # Query 6: Avg GPA of accepted Spring 2025
    cur.execute("""
        SELECT AVG(gpa) FROM applicants
        WHERE term ILIKE '%Spring 2025%'
        AND status ILIKE '%Accepted%'
        AND gpa IS NOT NULL
    """)
    avg_gpa_accepted = cur.fetchone()[0]

    # Query 7: JHU Masters Computer Science
    cur.execute("""
        SELECT COUNT(*) FROM applicants
        WHERE (university ILIKE '%JHU%'
                OR university ILIKE '%Johns Hopkins%'
                OR university ILIKE '%John Hopkins%'
                OR university ILIKE '%John Hopkin%'
                OR university ILIKE '%Johns Hopkin%')
        AND (degree ILIKE '%Master%' OR degree ILIKE '%MS%' OR degree ILIKE '%Masters%')
        AND program ILIKE '%Computer Science%'
    """)
    jhu_cs_masters = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "spring_2025_count": spring_2025_count,
        "percent_international": f"{percent_international:.2f}",
        "avg_gpa": f"{avgs['gpa']:.2f}" if avgs['gpa'] else "N/A",
        "avg_gre": f"{avgs['gre']:.2f}" if avgs['gre'] else "N/A",
        "avg_gre_v": f"{avgs['gre_v']:.2f}" if avgs['gre_v'] else "N/A",
        "avg_gre_aw": f"{avgs['gre_aw']:.2f}" if avgs['gre_aw'] else "N/A",
        "avg_gpa_american": f"{avg_gpa_american:.2f}" if avg_gpa_american else "N/A",
        "percent_accept_spring": f"{percent_accept_spring:.2f}",
        "avg_gpa_accepted": f"{avg_gpa_accepted:.2f}" if avg_gpa_accepted else "N/A",
        "jhu_cs_masters": jhu_cs_masters
    }

@app.route("/")
def home():
    """Main route for displaying results page."""
    results = get_results(ARGS)
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
