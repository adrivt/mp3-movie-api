# data_processor.py
import logging
import pandas as pd
from pandas.api.types import is_numeric_dtype


logger = logging.getLogger(__name__)

def remove_duplicates(df):
    before=len(df)
    df=df.drop_duplicates()
    after=len(df)
    logger.debug("Rows removed: %s", before-after)
    return df

def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    #before 
    beforecols=len(df.columns)
    beforerows=len(df)
    
    try:
        if axis not in ("rows", "columns"):
            raise ValueError(f"Unsupported axis: {axis}")
        df = df.dropna(axis=1) if axis == "columns" else df.dropna()
    except ValueError as e:
        logger.error(e, "Unsupported axis")
        raise
    removed = beforecols - len(df.columns) if axis == "columns" else beforerows - len(df)
    logger.debug(f"Removed {removed} {axis}")
    return df


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ["iqr", "zscore"]:
        logger.error("Method entered not valid")
        raise ValueError(f"Invalid method: {method}")
    else:
        try:
            if method== "iqr":
                for col in columns:
                    if col not in df.columns:
                        logger.warning("Column %s doesnt exist in the data", col)
                    elif not is_numeric_dtype(df[col]):
                        logger.warning("Column %s isnt numeric", col)
                    else:
                        q1 = df[col].quantile(0.25)
                        q3 = df[col].quantile(0.75)
                        iqr = q3 - q1
                        before=len(df)
                        lower = q1 -threshold*iqr
                        upper = q3 +threshold*iqr
                        df_score_cleaned = df[(df[col] >= lower) & (df[col] <= upper)]
                        after=len(df_score_cleaned)
                        logger.debug("Method: %s.  Threshold: %s. Rows removed: %s", method, threshold, before-after)
                        return df_score_cleaned
            else:
                for col in columns:
                    if col not in df.columns:
                        logger.warning("Column %s doesnt exist in the data", col)
                    elif not is_numeric_dtype(df[col]):
                        logger.warning("Column %s isnt numeric", col)
                    else:
                        mean = df[col].mean()
                        std = df[col].std()
                        z_scores = (df[col]-mean)/std
                        
                        before=len(df)
                        df_score_cleaned = df[z_scores.abs() <= threshold]
                        after=len(df_score_cleaned)
                        logger.debug("Method: %s.  Threshold: %s. Rows removed: %s", method, threshold, before-after)
                        return df_score_cleaned
        except ValueError: 
            logger.error("Something went wrong!")
            return df




def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    processing = config["processing"]

    if processing["remove_duplicates"]:
        df = remove_duplicates(df)

    missing = processing["missing"]
    if missing["enabled"]:
        df = handle_missing(df, axis=missing["axis"])

    outliers = processing["outliers"]
    if outliers["enabled"]:
        df = remove_outliers(
            df,
            columns=outliers["columns"],
            method=outliers["method"],
            threshold=outliers["threshold"],
        )

    return df
    


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "columns_removed": len(df_before.columns) - len(df_after.columns),
    }
