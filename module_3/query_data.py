import psycopg2
import argparse

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
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def count_spring_2025_entries(conn):
    """Counts number of applicants for Spring 2025.
    Original Question: How many entries do you have in your database who have applied for Fall 2024?
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM applicants
        WHERE term ILIKE '%Spring 2025%'
    """)
    result = cur.fetchone()[0]
    cur.close()
    print(f"Entries for Spring 2025: {result}")
    return result

def percent_international(conn):
    """Calculates percentage of international students (not American or Other).
    Original Question: What percentage of entries are from international students (not American or Other) (to two decimal places)?
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM applicants
        WHERE us_or_international ILIKE '%International%'
    """)
    international = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM applicants")
    total = cur.fetchone()[0]
    percent = (international / total) * 100 if total > 0 else 0
    cur.close()
    print(f"Percentage of international students: {percent:.2f}%")
    return round(percent, 2)

def average_metrics(conn):
    """Finds the average GPA, GRE, GRE V, and GRE AW for applicants who provided each metric.
    
    For each metric, calculates the average using only applicants who provided that metric.
    Original Question: What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?
    """
    cur = conn.cursor()
    # Individual averages, using only non-null values for each metric
    cur.execute("SELECT AVG(gpa) FROM applicants WHERE gpa IS NOT NULL")
    gpa = cur.fetchone()[0]
    cur.execute("SELECT AVG(gre) FROM applicants WHERE gre IS NOT NULL")
    gre = cur.fetchone()[0]
    cur.execute("SELECT AVG(gre_v) FROM applicants WHERE gre_v IS NOT NULL")
    gre_v = cur.fetchone()[0]
    cur.execute("SELECT AVG(gre_aw) FROM applicants WHERE gre_aw IS NOT NULL")
    gre_aw = cur.fetchone()[0]
    cur.close()
    print(f"Average GPA: {gpa:.2f}, GRE: {gre:.2f}, GRE V: {gre_v:.2f}, GRE AW: {gre_aw:.2f}")
    return gpa, gre, gre_v, gre_aw

def average_gpa_american_spring_2025(conn):
    """Finds average GPA of American students who applied for Spring 2025.
    Original Question: What is their average GPA of American students in Fall 2024?
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT AVG(gpa)
        FROM applicants
        WHERE us_or_international ILIKE '%American%'
        AND term ILIKE '%Spring 2025%'
        AND gpa IS NOT NULL
    """)
    result = cur.fetchone()[0]
    cur.close()
    print(f"Average GPA (American, Spring 2025): {result:.2f}")
    return result

def percent_acceptances_spring_2025(conn):
    """Percent of Spring 2025 entries that are Acceptances.
    Original Question: What percent of entries for Fall 2024 are Acceptances (to two decimal places)?
    """
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM applicants
        WHERE term ILIKE '%Spring 2025%'
    """)
    total = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(*) FROM applicants
        WHERE term ILIKE '%Spring 2025%'
        AND status ILIKE '%Accepted%'
    """)
    accepted = cur.fetchone()[0]
    percent = (accepted / total) * 100 if total > 0 else 0
    cur.close()
    print(f"Percent Acceptances (Spring 2025): {percent:.2f}%")
    return round(percent, 2)

def average_gpa_accepted_spring_2025(conn):
    """Average GPA of accepted applicants who applied for Spring 2025.
    Original Question: What is the average GPA of applicants who applied for Fall 2024 who are Acceptances?"""
    cur = conn.cursor()
    cur.execute("""
        SELECT AVG(gpa)
        FROM applicants
        WHERE term ILIKE '%Spring 2025%'
        AND status ILIKE '%Accepted%'
        AND gpa IS NOT NULL
    """)
    result = cur.fetchone()[0]
    cur.close()
    print(f"Average GPA (Accepted, Spring 2025): {result:.2f}")
    return result

def count_jhu_cs_masters(conn):
    """Counts entries for JHU, masters, Computer Science.
    Original Question: How many entries are from applicants who applied to JHU for a masters degrees in Computer Science?"""
    cur = conn.cursor()
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
    result = cur.fetchone()[0]
    cur.close()
    print(f"JHU Masters Computer Science applicants: {result}")
    return result

def parse_args():
    parser = argparse.ArgumentParser(description="Query applicant data from PostgreSQL.")
    parser.add_argument('--db_name', default='postgres', help='Database name')
    parser.add_argument('--db_user', default='postgres', help='Database user')
    parser.add_argument('--db_password', default='12345', help='Database password')
    parser.add_argument('--db_host', default='localhost', help='Database host')
    parser.add_argument('--db_port', default='5432', help='Database port')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    conn = create_connection(
        db_name=args.db_name,
        db_user=args.db_user,
        db_password=args.db_password,
        db_host=args.db_host,
        db_port=args.db_port
    )
    if conn:
        count_spring_2025_entries(conn)
        percent_international(conn)
        average_metrics(conn)
        average_gpa_american_spring_2025(conn)
        percent_acceptances_spring_2025(conn)
        average_gpa_accepted_spring_2025(conn)
        count_jhu_cs_masters(conn)
        conn.close()
