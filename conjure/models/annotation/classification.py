from typing import Literal
from pydantic import BaseModel, Field


class Classification(BaseModel):
    """
    Stores classification annotations and predictions.

    Attributes
    ----------
    `class_name : str`
        The name associated with the classification of the image.
    """

    annotation_type: Literal["Classification"] = Field(
        default="Classification", init=False
    )
    class_name: str
