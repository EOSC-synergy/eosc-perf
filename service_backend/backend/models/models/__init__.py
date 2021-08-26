"""Package with models definitions in modules."""
from datetime import datetime as dt

from sqlalchemy import Column, DateTime


class HasUploadDatetime(object):
    """Mixin that adds upload date."""
    # Better to use 'Upload' than 'Create' as the query parameter sort_by
    # is very complicate to reformat. i.e: "+created_at" -> "+upload_time" 

    #: (ISO8601) Upload datetime of the model instance
    upload_datetime = Column(DateTime, nullable=False, default=dt.now)
