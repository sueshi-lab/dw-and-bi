import glob
import json
import os
from typing import List

import psycopg2


def get_files(filepath: str) -> List[str]:
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files


def process(cur, conn, filepath):
    # Get list of files from filepath
    all_files = get_files(filepath)

    for datafile in all_files:
        with open(datafile, "r") as f:
            data = json.loads(f.read())
            for each in data:
                # Print some sample data
                
                if each["type"] == "IssueCommentEvent":
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                        each["payload"]["issue"]["url"],
                    )
                else:
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                    )

                # Insert data into actors
                insert_statement = f"""
                    INSERT INTO actors (
                        id,
                        login,
                        display_login,
                        url,
                        avatar_url
                    ) 
                    VALUES (
                        {each["actor"]["id"]}, 
                        '{each["actor"]["login"]}', 
                        '{each["actor"]["display_login"]}', 
                        '{each["actor"]["url"]}', 
                        '{each["actor"]["avatar_url"]}'
                    )
                    ON CONFLICT (id) DO NOTHING
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                # Insert data into repos
                insert_statement = f"""
                    INSERT INTO repos (
                        id,
                        name,
                        url
                    ) 
                    VALUES (
                        {each["repo"]["id"]}, 
                        '{each["repo"]["name"]}',  
                        '{each["repo"]["url"]}'
                    )
                    ON CONFLICT (id) DO NOTHING
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                # Insert data into orgs
                if "org" in each:
                    insert_statement = f"""
                        INSERT INTO orgs (
                            id,
                            login,
                            url,
                            avatar_url
                        ) 
                        VALUES (
                            {each["org"]["id"]}, 
                            '{each["org"]["login"]}',  
                            '{each["org"]["url"]}',  
                            '{each["org"]["avatar_url"]}'
                        )
                        ON CONFLICT (id) DO NOTHING
                    """
                else:
                    print("No 'org' information found in the object.", each["id"])
                # print(insert_statement)
                cur.execute(insert_statement)

                # Insert data into event_types
                insert_statement = f"""
                    INSERT INTO event_types (
                        name
                    ) 
                    SELECT '{each["type"]}'
                    WHERE NOT EXISTS (
                        SELECT 1 FROM event_types WHERE name = '{each["type"]}'
                    )
                    RETURNING id
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                # Finding event type id
                type_id_row = cur.fetchone()
                if type_id_row:
                    type_id = type_id_row[0]
                else:
                    select_event_type_statement = f"""
                        SELECT id FROM event_types WHERE name = '{each["type"]}'
                    """
                    cur.execute(select_event_type_statement)
                    type_id_row = cur.fetchone()
                    type_id = type_id_row[0] if type_id_row else None
                print(type_id)

                # Insert data into events
                insert_statement = f"""
                INSERT INTO events (
                        id,
                        type_id,
                        actor_id,
                        repo_id,
                        org_id,
                        is_public,
                        created_at
                    ) VALUES (
                        {each["id"]}, 
                        {type_id}, 
                        {each["actor"]["id"]},
                        {each["repo"]["id"]}, 
                        {'NULL' if "org" not in each or "id" not in each["org"] else each["org"]["id"]},
                        {each["public"]}, 
                        '{each["created_at"]}'
                    )
                    ON CONFLICT (id) DO NOTHING
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                conn.commit()


def main():
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    process(cur, conn, filepath="../data")

    conn.close()


if __name__ == "__main__":
    main()