"""Benchmark module"""
from sqlalchemy import Column, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declared_attr

from ..core import PkModel
from . import HasCreationDate
from .report import HasReports
from .user import HasCreationUser


class Benchmark(HasReports, HasCreationDate, HasCreationUser, PkModel):
    """The benchmark class represents a single type of benchmark that was run.

    Benchmarks are tied down to a specific docker image and version to avoid
    confusion and misleading comparisons in case a benchmark container changes
    its metrics or scoring scale between versions.
    
    It also includes a valid "JSON Schema" which is used to validate the
    results linked to the benchmark and uploaded into the system.

    Description is optional but offers a valuable text that can help possible
    users to understand the benchmark main features.
    """
    #: Docker image used to run/implement the benchmark
    docker_image = Column(Text, nullable=False)

    #: Docker image version/tag used of the benchmark
    docker_tag = Column(Text, nullable=False)

    #: Schema used to validate benchmark results before upload
    json_schema = Column(JSON, nullable=False)

    #: Short text describing the main benchmark features
    description = Column(Text, default="")

    @declared_attr
    def __table_args__(cls):
        mixin_indexes = list((HasCreationUser.__table_args__))
        mixin_indexes.extend([
            UniqueConstraint('docker_image', 'docker_tag')
        ])
        return tuple(mixin_indexes)

    def __repr__(self) -> str:
        """Get a human-readable representation string of the benchmark.

        Returns:
            str: A human-readable representation string of the benchmark.
        """
        return "<{} {}:{}>".format(
            self.__class__.__name__,
            self.docker_image,
            self.docker_tag
        )
