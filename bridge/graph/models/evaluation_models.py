from typing import List

from pydantic.v1 import BaseModel, Field


class RequirementsEval(BaseModel):
    is_complete: bool = Field("Flag to indicate if the requirements collection has been completed")


class CorrectionsEval(BaseModel):
    has_corrections: bool = Field("Flag to indicate if the user has indicated that there are corrections to be made")
    corrections: List[str] = Field("List of corrections to be made")