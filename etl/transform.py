# This file cleans, validates and preprocesses raw data for ML model

import pandas as pd  # data manipulation library
from sklearn.preprocessing import LabelEncoder  # encode categorical columns to numbers
import os  # access environment variables
import sys  # system path manipulation

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # add root to path
from utils.logger import get_logger  # import common logger

logger = get_logger(__name__)  # get logger for this module


def validate_data(df):
    # data validation — check schema, types, nulls, value ranges
    try:
        # check required columns exist
        required_columns = [
            "Administrative",
            "Administrative_Duration",
            "Informational",
            "Informational_Duration",
            "ProductRelated",
            "ProductRelated_Duration",
            "BounceRates",
            "ExitRates",
            "PageValues",
            "SpecialDay",
            "Month",
            "OperatingSystems",
            "Browser",
            "Region",
            "TrafficType",
            "VisitorType",
            "Weekend",
            "Revenue",
        ]

        missing_cols = [col for col in required_columns if col not in df.columns]

        if missing_cols:
            raise ValueError(f"Missing columns: {missing_cols}")

        logger.info("Column validation passed")
        print("✅ Column validation passed")

        # check null values
        null_counts = df.isnull().sum()

        if null_counts.any():
            logger.warning(f"Null values found: {null_counts[null_counts > 0].to_dict()}")
            print(f"⚠️ Null values found: {null_counts[null_counts > 0].to_dict()}")
        else:
            logger.info("Null value validation passed")
            print("✅ Null value validation passed")

        # check BounceRates and ExitRates are between 0 and 1
        if not df["BounceRates"].between(0, 1).all():
            logger.warning("BounceRates contains values outside 0-1 range")
            print("⚠️ BounceRates contains values outside 0-1 range")

        if not df["ExitRates"].between(0, 1).all():
            logger.warning("ExitRates contains values outside 0-1 range")
            print("⚠️ ExitRates contains values outside 0-1 range")

        logger.info("Value range validation passed")
        print("✅ Value range validation passed")

        # check Revenue column has only 0 and 1
        if not df["Revenue"].isin([0, 1]).all():
            raise ValueError("Revenue column contains invalid values — expected 0 or 1")

        logger.info("Revenue column validation passed")
        print("✅ Revenue column validation passed")

        # check row count
        if len(df) == 0:
            raise ValueError("Dataframe is empty — no data to process")

        logger.info(f"Row count validation passed — {len(df)} rows")
        print(f"✅ Row count validation passed — {len(df)} rows")

    except Exception as e:
        logger.error(f"Data validation failed: {e}")
        print(f"❌ Data validation failed: {e}")
        raise


def transform_data(df):
    try:
        logger.info("Starting data transformation")
        print("🚀 Starting data transformation")

        # validate data before transformation
        validate_data(df)

        # drop duplicate rows if any
        before = len(df)
        df = df.drop_duplicates()

        logger.info(f"Dropped {before - len(df)} duplicate rows")
        print(f"✅ Dropped {before - len(df)} duplicate rows")

        # drop rows where any value is null
        before = len(df)
        df = df.dropna()

        logger.info(f"Dropped {before - len(df)} null rows")
        print(f"✅ Dropped {before - len(df)} null rows")

        # encode Month column
        le_month = LabelEncoder()
        df["Month"] = le_month.fit_transform(df["Month"])

        logger.info("Month column encoded")
        print("✅ Month column encoded")

        # encode VisitorType column
        le_visitor = LabelEncoder()
        df["VisitorType"] = le_visitor.fit_transform(df["VisitorType"])

        logger.info("VisitorType column encoded")
        print("✅ VisitorType column encoded")

        # convert Weekend column to integer
        df["Weekend"] = df["Weekend"].astype(int)

        # convert Revenue column to integer
        df["Revenue"] = df["Revenue"].astype(int)

        logger.info(f"Transformation complete — final shape: {df.shape}")
        print(f"✅ Transformation complete — final shape: {df.shape}")

        return df

    except Exception as e:
        logger.error(f"Data transformation failed: {e}")
        print(f"❌ Data transformation failed: {e}")
        raise


if __name__ == "__main__":
    from extract import extract_data

    df = extract_data()
    df = transform_data(df)

    print(df.head())
    print(df.dtypes)
