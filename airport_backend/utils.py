import os
from slugify import slugify
import uuid


def create_custom_path(instance, filename,):
    _, extension = os.path.splitext(filename)
    return os.path.join(
            f"uploads/images/{instance.__class__.__name__.lower()}",
            f"{slugify(instance.full_name)}-{uuid.uuid4()}{extension}"
        )