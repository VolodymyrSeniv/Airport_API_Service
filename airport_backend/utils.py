import os
from slugify import slugify
import uuid


def create_custom_path_crew(instance, filename,):
    _, extension = os.path.splitext(filename)
    return os.path.join(
            "uploads/images/crews",
            f"{slugify(instance.full_name)}-{uuid.uuid4()}{extension}"
        )


def create_custom_path_airplane(instance, filename,):
    _, extension = os.path.splitext(filename)
    return os.path.join(
            "uploads/images/airplanes",
            f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
        )