"""Models module package for main models definition."""
import jsonschema
from flask_smorest import abort
from jsonschema.exceptions import ValidationError
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, relationship

from ..core import PkModel
from . import HasUploadDatetime
from .report import HasReports
from .tag import HasTags
from .user import HasUploader


class Result(HasReports, HasTags, HasUploadDatetime, HasUploader, PkModel):
    """The Result model represents the results of the execution of a 
    specific Benchmark on a specific Site and Flavor. 

    They carry the JSON data output by the executed benchmarks.

    **Properties**:
    """
    #: (JSON, required) Benchmark execution results
    json = Column(JSONB, nullable=False)

    #: (ISO8601, required) Benchmark execution **START**
    execution_datetime = Column(DateTime, nullable=False)

    #: (Benchmark, required) Benchmark used to provide the results
    benchmark = relationship("Benchmark", backref=backref(
        "_results", cascade="all, delete-orphan"
    ))
    _benchmark_id = Column(ForeignKey('benchmark.id'), nullable=False)

    #: (Read_only) Docker image of used benchmark
    docker_image = association_proxy('benchmark', 'docker_image')

    #: (Read_only) Docker tag of used benchmark
    docker_tag = association_proxy('benchmark', 'docker_tag')

    #: (Site, required) Site where the benchmark was executed
    site = relationship("Site", backref=backref(
        "_results", cascade="all, delete-orphan"
    ))
    _site_id = Column(ForeignKey('site.id'), nullable=False)

    #: (Read_only) Name of the site where the benchmar was executed
    site_name = association_proxy('site', 'name')

    #: (Flavor, required) Flavor used to executed the benchmark 
    flavor = relationship("Flavor", backref=backref(
        "_results", cascade="all, delete-orphan"
    ))
    _flavor_id = Column(ForeignKey('flavor.id'), nullable=False)

    #: (Read_only) Name of the flavor used to executed the benchmark 
    flavor_name = association_proxy('flavor', 'name')

    def __init__(self, **properties):
        """Validates the result passes the benchmark JSON Schema and sets
        default reports to empty list.
        """
        benchmark = properties['benchmark']
        json = properties['json']
        if not 'reports' in properties:
            properties['reports'] = []
        try:
            jsonschema.validate(json, schema=benchmark.json_schema)
        except ValidationError as err:
            abort(422, messages={'error': err.message, 'path': f"{err.path}"})
        super().__init__(**properties)

    def __repr__(self) -> str:
        """Human-readable representation string"""
        return "<{} {}>".format(self.__class__.__name__, self.json)
