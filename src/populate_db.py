from db import conn
import pandas
from psycopg2.extras import execute_values

transactions_file = '../data/transactional-sample.csv'
df = pandas.read_csv(transactions_file, dtype={'device_id': str})

cursor = conn.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(10) PRIMARY KEY,
    merchant_id VARCHAR(10),
    user_id VARCHAR(10),
    card_number VARCHAR(20),
    transaction_date TIMESTAMP,
    transaction_amount NUMERIC(10, 2),
    device_id  VARCHAR(10),
    has_cbk BOOLEAN
);
"""

cursor.execute(create_table_query)
conn.commit()

tuples = [tuple(x) for x in df.to_numpy()]


insert_query = """
INSERT INTO transactions (transaction_id, merchant_id, user_id, card_number, transaction_date, transaction_amount, device_id, has_cbk) VALUES %s;
"""

execute_values(cursor, insert_query, tuples)
conn.commit()

cursor.close()
conn.close()
