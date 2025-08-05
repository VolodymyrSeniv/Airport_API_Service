import os
import uuid
from django.utils.text import slugify

def create_custom_path(instance, filename):
    _, extension = os.path.splitext(filename)
    base_name = getattr(instance, 'full_name', None) or getattr(instance, 'name', 'unknown')
    slugified_name = slugify(base_name)
    class_name = instance.__class__.__name__.lower()
    return os.path.join(
        f"uploads/images/{class_name}",
        f"{slugified_name}-{uuid.uuid4()}{extension}"
    )
