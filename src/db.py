import psycopg2

db_config = {
    'dbname': 'risk_analysis',
    'user': 'postgres',
    'password': '25011961',
    'host': 'localhost'
}

conn = psycopg2.connect(**db_config)
