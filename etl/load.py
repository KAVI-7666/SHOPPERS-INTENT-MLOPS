# This file loads transformed data into PostgreSQL data warehouse

import pandas as pd  # data manipulation
from sqlalchemy import create_engine  # database connection engine
from dotenv import load_dotenv  # load environment variables
import os  # access environment variables
import sys  # system path manipulation
from urllib.parse import quote_plus

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # add root to path
from utils.logger import get_logger  # import common logger

load_dotenv()  # load .env file

logger = get_logger(__name__)  # get logger for this module
password = quote_plus(os.getenv("DB_PASSWORD"))


def get_mysql_engine():
    try:
        # build mysql connection string for source database
        url = (
            f"mysql+pymysql://{os.getenv('DB_USER')}:{password}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        engine = create_engine(url)  # return mysql engine
        logger.info("MySQL engine created successfully")
        print("✅ MySQL engine created successfully")
        return engine
    except Exception as e:
        logger.error(f"Failed to create MySQL engine: {e}")
        print(f"❌ Failed to create MySQL engine: {e}")
        raise


def get_pg_engine():
    try:
        # build postgresql connection string for data warehouse
        url = (
            f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
            f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_NAME')}"
        )
        engine = create_engine(url)  # return postgresql engine
        logger.info("PostgreSQL engine created successfully")
        print("✅ PostgreSQL engine created successfully")
        return engine
    except Exception as e:
        logger.error(f"Failed to create PostgreSQL engine: {e}")
        print(f"❌ Failed to create PostgreSQL engine: {e}")
        raise


def load_data(df):
    try:
        pg_engine = get_pg_engine()  # get postgresql connection

        df.to_sql(
            "transformed_shoppers",  # table name in postgresql
            pg_engine,  # postgresql engine
            if_exists="replace",  # drop and recreate table every time
            index=False,  # do not write index column
        )

        logger.info(f"Loaded {len(df)} rows into PostgreSQL warehouse")
        print(f"✅ Loaded {len(df)} rows into PostgreSQL warehouse")

    except Exception as e:
        logger.error(f"Failed to load data into PostgreSQL: {e}")
        print(f"❌ Failed to load data into PostgreSQL: {e}")
        raise


if __name__ == "__main__":
    from extract import extract_data  # import extract function
    from transform import transform_data  # import transform function

    df = extract_data()  # extract raw data from mysql
    df = transform_data(df)  # clean and encode data
    load_data(df)  # load into postgresql warehouse
