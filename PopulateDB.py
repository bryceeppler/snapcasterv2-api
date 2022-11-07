"""
PopulateDB.py

This is a script to update the set table in the database.
Every time a new set is released, this script should be run to update the database.
The SetList.json file is from MTGJSON and is used to get the set codes and names.

In the future I would like to set up a script to run this automatically when a new set is released.

Instructions:
Download SetList.json from MtgJson and place it in the same directory as this script and the .env file.
Run python PopulateDB.py
"""
# script to populate the database with the setList json file
import json
import psycopg2
import os
import dotenv

dotenv.load_dotenv()

# Connect to the database
conn = psycopg2.connect(
    dbname=os.environ['PG_DB'],
    user=os.environ['PG_USER'],
    password=os.environ['PG_PASSWORD'],
    host=os.environ['PG_HOST'],
    port=os.environ['PG_PORT']
)
cur = conn.cursor()

# Open the json file
with open('SetList.json') as f:
    data = json.load(f)

cur.execute("""
    CREATE TABLE IF NOT EXISTS set (
        id SERIAL,
        name VARCHAR(255) NOT NULL,
        base_set_size INTEGER NOT NULL,
        total_set_size INTEGER NOT NULL,
        code VARCHAR(20),
        release_date DATE NOT NULL,
        type VARCHAR(255) NOT NULL,
        PRIMARY KEY (name, base_set_size, code, release_date, type)
    );
""")
conn.commit()

# Insert the data into the database, no duplicates
for item in data['data']:
    try:
        if item['type'] in ["token", "memorabilia", "starter", "spellbook", "promo", "alchemy", "archenemy", "arsenal", "box", "duel_deck", "from_the_vault", "planechase", "premium_deck", "funny", "commander", "vanguard", "treasure_chest", "masterpiece"]:
            continue
        # If a duplicate row is found, skip it
        cur.execute("""
            INSERT INTO set (name, base_set_size, total_set_size, code, release_date, type)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (item['name'], item['baseSetSize'], item['totalSetSize'], item['code'], item['releaseDate'], item['type']))
    except IndexError as e:
        print(e)
        conn.rollback()
    except Exception as e:
        print(e)
        conn.rollback()
    else:
        conn.commit()

# Commit the changes to the database
conn.commit()
cur.close()
conn.close()