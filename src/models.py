#It’s the file that defines the shape of the data going in and out of your API.
#“An upload response looks like this.” “A health check looks like that.” Everything else in the project can then trust those shapes.

from pydantic import BaseModel, Field
class HealthResponse(BaseModel):
    status: str
    version: str


class DatasetInfo(BaseModel):
    # TODO: id (int), filename (str), rows (int),
    # columns (int), column_names (list[str])
    id: int
    filename: str
    rows: int
    columns: int
    column_names: list[str]


class ValidationSettings(BaseModel):
    required_columns: list[str] = Field(default_factory=list)
    numeric_columns: list[str] = Field(default_factory=list)

class MissingSettings(BaseModel):
    enabled: bool = True
    axis: str = "rows"

class OutlierSettings(BaseModel):
    enabled: bool = False
    columns: list[str] = Field(default_factory=list)
    method: str = "iqr"
    threshold: float = 1.5

class ProcessingSettings(BaseModel):
    remove_duplicates: bool = True
    missing: MissingSettings = Field(default_factory=MissingSettings)
    outliers: OutlierSettings = Field(default_factory=OutlierSettings)

class ProcessConfig(BaseModel):
    # TODO: Define these fields:
    # validation: ValidationSettings
    # processing: ProcessingSettings
    # Use Field(default_factory=ModelName) for each default.
    validation: ValidationSettings=Field(default_factory=ValidationSettings)
    processing: ProcessingSettings=Field(default_factory=ProcessingSettings)
    
class ProcessingReport(BaseModel):
    # TODO: Define these required fields without defaults:
    # id: int
    validation_rows_removed: int
    cleaning_report: dict[str, int]
    id: int

class MovieUploadInfo(BaseModel):
    filename: str
    rows: int
    columns: int
    column_names: list[str]


class MovieDataResponse(BaseModel):
    data: list[dict]
    total_rows: int


class MovieProcessingReport(BaseModel):
    validation_rows_removed: int
    cleaning_report: dict
