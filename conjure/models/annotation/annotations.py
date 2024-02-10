from typing import Annotated
from pydantic import BaseModel, Field

from conjure.models.annotation.classification import Classification
from conjure.models.annotation.object_detection import ObjectDetection


class Annotations(BaseModel):
    """
    Holds a collection of annotations for a single image.
    """

    annotations: list[
        Annotated[
            Classification | ObjectDetection, Field(discriminator="annotation_type")
        ]
    ]
