"""Models module package for main models definition."""
import jsonschema
from flask_smorest import abort
from jsonschema.exceptions import ValidationError
from sqlalchemy import (Column, DateTime, ForeignKey, ForeignKeyConstraint,
                        select)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import backref, column_property, relationship

from ..core import PkModel
from .benchmark import Benchmark
from .flavor import Flavor
from .reports import HasClaims
from .site import Site
from .tag import HasTags
from .user import HasUploader


class Result(HasClaims, HasTags, HasUploader, PkModel):
    """The Result model represents the results of the execution of a
    specific Benchmark on a specific Site and Flavor.

    They carry the JSON data output by the executed benchmarks.

    **Properties**:
    """
    #: (JSON, required) Benchmark execution results
    json = Column(JSONB, nullable=False)

    #: (ISO8601, required) Benchmark execution **START**
    execution_datetime = Column(DateTime, nullable=False)

    #: (Conflicts Benchmark) Id of the benchmar used
    benchmark_id = Column(ForeignKey('benchmark.id'), nullable=False)

    #: (Benchmark, required) Benchmark used to provide the results
    benchmark = relationship("Benchmark", backref=backref(
        "_results", cascade="all, delete-orphan"
    ))
    benchmark_name = column_property(
        select([Benchmark.name]).where(Benchmark.id == benchmark_id).
        scalar_subquery()
    )

    #: (Conflicts Flavor) Id of the flavor used to executed the benchmark
    flavor_id = Column(ForeignKey('flavor.id'), nullable=False)

    #: (Flavor, required) Flavor used to executed the benchmark
    flavor = relationship("Flavor", backref=backref(
        "_results", cascade="all, delete-orphan",
    ))
    flavor_name = column_property(
        select([Flavor.name]).where(Flavor.id == flavor_id).
        scalar_subquery()
    )

    #: (Collected from flavor) Id of the site where the benchmar was executed
    site_id = Column(ForeignKey('site.id'), nullable=False)

    #: (Collected from flavor) Site where the benchmark was executed
    site = relationship("Site", backref=backref(
        "_results", cascade="all, delete-orphan"
    ))
    site_name = column_property(
        select([Site.name]).where(Site.id == site_id).
        scalar_subquery()
    )
    site_address = column_property(
        select([Site.address]).where(Site.id == site_id).
        scalar_subquery()
    )

    __table_args__ = (
        ForeignKeyConstraint(['uploader_iss', 'uploader_sub'],
                             ['user.iss', 'user.sub']),
    )

    def __init__(self, site=None, site_id=None, **properties):
        """Validates the result passes the benchmark JSON Schema and sets
        default reports to empty list.
        """
        benchmark, json = properties['benchmark'], properties['json']
        try:
            jsonschema.validate(json, schema=benchmark.json_schema)
        except ValidationError as err:
            abort(422, messages={'error': err.message, 'path': f"{err.path}"})

        if site or site_id:
            raise KeyError("Site is collected from flavor")
        properties['site'] = properties['flavor'].site
        properties['site_id'] = properties['flavor'].site_id

        super().__init__(**properties)

    def __repr__(self) -> str:
        """Human-readable representation string"""
        return "<{} {}>".format(self.__class__.__name__, self.json)
