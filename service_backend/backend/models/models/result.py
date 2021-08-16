"""Models module package for main models definition."""
import jsonschema
import sqlalchemy as sa
from flask_smorest import abort
from jsonschema.exceptions import ValidationError
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, relationship

from ..core import PkModel
from ..utils import HasCreationDate
from .report import HasReports
from .tag import HasTags
from .user import HasCreationUser


class Result(HasReports, HasTags, HasCreationDate, HasCreationUser, PkModel):
    """The Result class represents a single benchmark result and its contents.

    They carry the JSON data output by the ran benchmarks.
    """
    json = Column(JSONB, nullable=False)
    executed_at = Column(DateTime, nullable=False)

    benchmark_id = Column(ForeignKey('benchmark.id'), nullable=False)
    benchmark = relationship("Benchmark", backref=backref(
        "results", cascade="all, delete-orphan"
    ))
    docker_image = association_proxy('benchmark', 'docker_image')
    docker_tag = association_proxy('benchmark', 'docker_tag')

    site_id = Column(ForeignKey('site.id'), nullable=False)
    site = relationship("Site", backref=backref(
        "results", cascade="all, delete-orphan"
    ))
    site_name = association_proxy('site', 'name')

    flavor_id = Column(ForeignKey('flavor.id'), nullable=False)
    flavor = relationship("Flavor", backref=backref(
        "results", cascade="all, delete-orphan"
    ))
    flavor_name = association_proxy('flavor', 'name')

    def __repr__(self) -> str:
        """Get a human-readable representation string of the result.

        Returns:
            str: A human-readable representation string of the result.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.id)

    @classmethod
    def create(cls, benchmark, json, **kwargs):
        try:
            jsonschema.validate(json, schema=benchmark.json_schema)
        except ValidationError as err:
            abort(422, messages={'error': err.message, 'path': f"{err.path}"})

        return super().create(benchmark=benchmark, json=json, **kwargs)

    @classmethod
    def search(cls, terms):
        """Query all results containing all keywords in the columns.

        Args:
            terms (List[str]): A list of all keywords that need to be matched.
        Returns:
            List[Result]: A list containing all matching query results in the
            database.
        """
        results = cls.query
        for keyword in terms:
            results = results.filter(
                sa.or_(
                    Result.docker_image.contains(keyword),
                    Result.docker_tag.contains(keyword),
                    Result.site_name.contains(keyword),
                    Result.flavor_name.contains(keyword),
                    Result.tag_names == keyword
                ))

        return results
