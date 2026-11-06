# src/data_validator.py
import logging
import pandas as pd


logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data.

    required_columns: a list of column names that must exist.
    numeric_columns: a list of column names whose values should be numeric.
    """
    #Check that every name in required_columns exists in the DataFrame
    missing = set(required_columns) - set(df.columns)
    if missing:
        logger.error(f"Missing required columns: {sorted(missing)}")
        raise ValueError(f"Columns missing: {sorted(missing)}")
    
    """ identify non-missing values that cannot be converted to a number.
    Log a WARNING and remove rows containing those invalid numeric values.
    After removing invalid values, convert each configured numeric column to a numeric data type."""
    
    for col in numeric_columns:
        invalid_rows = []
        for i, value in df[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except ValueError:
                    # TODO: Log a warning and record this row's index.
                    logger.error(f"Row number {i} cannot be converted to float.")
                    invalid_rows.append(i)
        
        # TODO: Remove the invalid rows.
        df = df.drop(invalid_rows)


        #convert to a numeric data type
        df[col] = pd.to_numeric(df[col])

        logger.debug(f"Valid rows: {len(df)}. Deleted rows: {len(invalid_rows)}")
        return df
