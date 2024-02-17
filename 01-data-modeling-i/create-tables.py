from typing import NewType

import psycopg2


PostgresCursor = NewType("PostgresCursor", psycopg2.extensions.cursor)
PostgresConn = NewType("PostgresConn", psycopg2.extensions.connection)

table_drop_events = "DROP TABLE IF EXISTS events"
table_drop_actors = "DROP TABLE IF EXISTS actors"
table_drop_repos = "DROP TABLE IF EXISTS repos"
table_drop_orgs = "DROP TABLE IF EXISTS orgs"
table_drop_event_types = "DROP TABLE IF EXISTS event_types"

table_create_actors = """
    CREATE TABLE IF NOT EXISTS actors (
        id int,
        login text,
        display_login text,
        url text,
        avatar_url text,
        PRIMARY KEY(id)
    )
"""
table_create_repos = """
    CREATE TABLE IF NOT EXISTS repos (
        id int,
        name text,
        url text,
        PRIMARY KEY(id)
    )
"""
table_create_orgs = """
    CREATE TABLE IF NOT EXISTS orgs (
        id int,
        login text,
        url text,
        avatar_url text,
        PRIMARY KEY(id)
    )
"""
table_create_events = """
    CREATE TABLE IF NOT EXISTS events (
        id BIGINT,
        type_id int,
        actor_id int,
        repo_id int,
        org_id int,
        created_at timestamp,
        PRIMARY KEY(id),
        CONSTRAINT fk_type FOREIGN KEY(type_id) REFERENCES event_types(id),
        CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id),
        CONSTRAINT fk_repo FOREIGN KEY(repo_id) REFERENCES repos(id),
        CONSTRAINT fk_org FOREIGN KEY(org_id) REFERENCES orgs(id)
    )
"""
table_create_event_types = """
    CREATE TABLE IF NOT EXISTS event_types (
        id SERIAL PRIMARY KEY,
        name text
    )
"""

create_table_queries = [
    table_create_actors,
    table_create_repos,
    table_create_orgs,
    table_create_event_types,
    table_create_events,
]
drop_table_queries = [
    table_drop_events,
    table_drop_actors,
    table_drop_repos,
    table_drop_orgs,
    table_drop_event_types,
]


def drop_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database.
    - Establishes connection with the sparkify database and gets
    cursor to it.
    - Drops all the tables.
    - Creates all tables needed.
    - Finally, closes the connection.
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()