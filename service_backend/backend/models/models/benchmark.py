"""Benchmark module"""
import jsonschema
import sqlalchemy as sa
from flask_smorest import abort
from jsonschema.exceptions import SchemaError
from sqlalchemy import Column, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declared_attr

from ..core import PkModel
from ..utils import HasCreationDate, dockerhub
from .report import HasReports
from .user import HasCreationUser


class Benchmark(HasReports, HasCreationDate, HasCreationUser, PkModel):
    """The benchmark class represents a single type of benchmark that was run.

    Benchmarks are tied down to a specific docker image version to avoid
    confusion and misleading comparisons in case the benchmark images change
    their metrics or scoring scale from version to version.
    """
    docker_image = Column(Text, nullable=False)
    docker_tag = Column(Text, nullable=False)
    description = Column(Text, default="")
    json_schema = Column(JSON, nullable=False)

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

    @classmethod
    def create(cls, docker_image, docker_tag, json_schema, **kwargs):
        if not dockerhub.valid_image(docker_image, docker_tag):
            abort(422, messages={'error': "Unknown docker image"})
        try:
            jsonschema.Draft7Validator.check_schema(json_schema)
        except SchemaError as err:
            abort(422, messages={'error': err.message, 'path': f"{err.path}"})

        return super().create(
            docker_image=docker_image, docker_tag=docker_tag,
            json_schema=json_schema, **kwargs
        )

    @classmethod
    def search(cls, terms):
        """Query all benchmarks containing all keywords in the name.

        Args:
            terms (List[str]): A list of all keywords that need to be in the
            benchmark's docker name.
        Returns:
            List[Benchmark]: A list containing all matching benchmarks in the
            database.
        """
        results = cls.query
        for keyword in terms:
            results = results.filter(
                sa.or_(
                    Benchmark.docker_image.contains(keyword),
                    Benchmark.docker_tag.contains(keyword),
                    Benchmark.description.contains(keyword)
                ))

        return results
