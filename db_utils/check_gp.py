import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import GP_USER, GP_PASSWORD, GP_HOST, GP_PORT, DB_NAME, WEATHER_TABLE_NAME


db_config = {
    "user": GP_USER,
    "password": GP_PASSWORD,
    "host": GP_HOST,
    "port": GP_PORT,
}

def create_database():
    try:
        conn = psycopg2.connect(dbname="postgres", **db_config)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"База данных {DB_NAME} создана.")
        else:
            print(f"База данных {DB_NAME} уже существует.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Ошибка при создании базы данных: {e}")


def create_schema_and_table():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, **db_config)
        cur = conn.cursor()

        cur.execute(f"""
            SELECT 1
            FROM information_schema.schemata
            WHERE schema_name = '{DB_NAME}';
        """)
        schema_exists = cur.fetchone()

        if not schema_exists:
            cur.execute(f"CREATE SCHEMA {DB_NAME};")
            print(f"Схема {DB_NAME} создана.")
        else:
            print(f"Схема {DB_NAME} уже существует.")

        cur.execute(f"""
            CREATE SCHEMA IF NOT EXISTS {DB_NAME};

            CREATE TABLE IF NOT EXISTS {DB_NAME}.{WEATHER_TABLE_NAME} (
                observation_id SERIAL PRIMARY KEY,
                country VARCHAR(2),
                city VARCHAR(64),
                timestamp_utc TIMESTAMP NOT NULL,
                temperature NUMERIC(5,2),
                feels_like NUMERIC(5,2),
                pressure INTEGER,
                humidity INTEGER,
                weather_main VARCHAR(32),
                weather_description VARCHAR(128),
                wind_speed NUMERIC(5,2),
                wind_deg INTEGER,
                clouds INTEGER,
                ingestion_time TIMESTAMP DEFAULT NOW()
            );
        """)

        conn.commit()
        print("Схема и таблица успешно созданы.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Ошибка при создании схемы или таблицы: {e}")

def create_db_schema_table():
    create_database()
    create_schema_and_table()