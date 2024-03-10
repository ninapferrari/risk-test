import db
import pandas as pd
from psycopg2.extras import execute_values

transactions_file = '../data/transactional-sample.csv'
df = pd.read_csv(transactions_file, dtype={'device_id': str})

cursor = db.conn.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(10) PRIMARY KEY,
    merchant_id VARCHAR(10),
    user_id VARCHAR(10),
    card_number VARCHAR(20),
    transaction_date TIMESTAMP,
    transaction_amount NUMERIC,
    device_id  VARCHAR(20),
    has_cbk BOOLEAN
);
"""

cursor.execute(create_table_query)
db.conn.commit()

tuples = [tuple(x) for x in df.to_numpy()]


insert_query = """
INSERT INTO transactions (transaction_id, merchant_id, user_id, card_number, transaction_date, transaction_amount, device_id, has_cbk) VALUES %s;
"""

execute_values(cursor, insert_query, tuples)
db.conn.commit()

cursor.close()
db.conn.close()