import psycopg2

from pinga.config import get_pg_uri

QUERY_CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS pinga_events (
    id SERIAL PRIMARY KEY,
    check_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    url TEXT NOT NULL,
    status TEXT NOT NULL,
    http_status INTEGER,
    response_time_seconds FLOAT,
    error_message TEXT
);
"""

QUERY_INSERT_EVENT = """
INSERT INTO pinga_events (url, status, http_status, response_time_seconds)
VALUES (%s, %s, %s, %s);
"""

QUERY_INSERT_ERROR_EVENT = """
INSERT INTO pinga_events (url, status, error_message)
VALUES (%s, %s, %s);
"""


def get_db_conn():
    return psycopg2.connect(get_pg_uri())


def drop_events_table(conn):
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS pinga_events;")
    conn.commit()

    cursor.close()


def create_events_table(conn):
    cursor = conn.cursor()

    cursor.execute(QUERY_CREATE_EVENTS_TABLE)
    conn.commit()

    cursor.close()


def save_event(conn, event):
    if event["status"] == "error":
        _insert_error_event(conn, event)
    else:
        _insert_event(conn, event)


def _insert_event(conn, event):
    cursor = conn.cursor()

    cursor.execute(
        QUERY_INSERT_EVENT,
        (
            event["url"],
            event["status"],
            event["httpStatus"],
            event["responseTimeSeconds"]
        )
    )
    conn.commit()

    cursor.close()


def _insert_error_event(conn, event):
    cursor = conn.cursor()

    cursor.execute(
        QUERY_INSERT_ERROR_EVENT,
        (
            event["url"],
            event["status"],
            event["errorMessage"],
        )
    )
    conn.commit()

    cursor.close()
