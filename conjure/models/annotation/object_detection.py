from typing import Literal
from pydantic import BaseModel, Field

from conjure.models.annotation.bounding_box import BoundingBox


class ObjectDetection(BaseModel):
    """
    Stores an object detection annotation or prediction.

    Attributes
    ----------
    `class_name: str`
        A string depicting the type of object.

    `bounding_box : BoundingBox`
        Bounding box of an object in the image.
    """

    annotation_type: Literal["ObjectDetection"] = Field(
        default="ObjectDetection", init=False
    )
    class_name: str
    bounding_box: BoundingBox
