from config import GP_URL, GP_USER, GP_PASSWORD, DB_TABLE

def get_postgres_properties():
    return {
        "url": GP_URL,
        "db.table": DB_TABLE,
        "user": GP_USER,
        "password": GP_PASSWORD,
        "driver": "org.postgresql.Driver"
    }
