"""Benchmark module"""
import jsonschema
from flask_smorest import abort
from jsonschema.exceptions import SchemaError
from sqlalchemy import Column, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declared_attr

from ..core import PkModel
from . import HasCreationDate
from .report import HasReports
from .user import HasCreationUser


class Benchmark(HasReports, HasCreationDate, HasCreationUser, PkModel):
    """The benchmark model represents a single type of docker container 
    designed to run and produce benchmark results from virtual machines.

    Benchmarks are tied down to a specific docker image and version to avoid
    confusion and misleading comparisons in case a benchmark container changes
    its metrics or scoring scale between versions.
    
    It also includes a valid "JSON Schema" which is used to validate the
    results linked to the benchmark and uploaded into the system.

    Description is optional but offers a valuable text that can help possible
    users to understand the benchmark main features.

    **Properties**:
    """
    #: (Text, required) Docker image referenced by the benchmark
    docker_image = Column(Text, nullable=False)

    #: (Text, required) Docker image version/tag referenced by the benchmark
    docker_tag = Column(Text, nullable=False)

    #: (JSON, required) Schema used to validate benchmark results before upload
    json_schema = Column(JSON, nullable=False)

    #: (Text) Short text describing the main benchmark features
    description = Column(Text, default="")

    @declared_attr
    def __table_args__(cls):
        mixin_indexes = list((HasCreationUser.__table_args__))
        mixin_indexes.extend([
            UniqueConstraint('docker_image', 'docker_tag')
        ])
        return tuple(mixin_indexes)

    def __init__(self, **properties):
        """Check the included schema is valid."""
        json_schema = properties['json_schema']
        try:
            jsonschema.Draft7Validator.check_schema(json_schema)
        except SchemaError as err:
            abort(422, messages={'error': err.message, 'path': f"{err.path}"})
        super().__init__(**properties)

    def __repr__(self) -> str:
        """Human-readable representation string"""
        return "<{} {}:{}>".format(
            self.__class__.__name__,
            self.docker_image,
            self.docker_tag
        )
