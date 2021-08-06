"""Models module package for main models definition."""
from flask_smorest import abort
from sqlalchemy import Column, ForeignKey, Text, UniqueConstraint, or_
from sqlalchemy.dialects.postgresql import JSON, JSONB
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship

from . import PkModel
from .utils import dockerhub
from .utils.reports import HasReports, Report
from .utils.tags import HasTags, Tag
from .utils.users import User
from .utils.utils import HasCreationDetails

__all__ = [
    "Result", "Benchmark", "Site", "Flavor",
    "User", "Report", "Tag"
]


# --------------------------------------------------------------------
# BENCHMARK model

class Benchmark(HasReports, HasCreationDetails, PkModel):
    """The benchmark class represents a single type of benchmark that was run.

    Benchmarks are tied down to a specific docker image version to avoid
    confusion and misleading comparisons in case the benchmark images change
    their metrics or scoring scale from version to version.
    """
    docker_image = Column(Text, nullable=False)
    docker_tag = Column(Text, nullable=False)
    description = Column(Text, default="")
    json_template = Column(JSON, default={})

    @declared_attr
    def __table_args__(cls):
        mixin_indexes = list((HasCreationDetails.__table_args__))
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
    def create(cls, docker_image, docker_tag="latest", **kwargs):
        if not dockerhub.valid_image(docker_image, docker_tag):
            abort(422, messages={'error': "Unknown docker image"})
        else:
            return super().create(
                docker_image=docker_image,
                docker_tag=docker_tag,
                **kwargs
            )

    @classmethod
    def query_with(cls, terms):
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
                or_(
                    Benchmark.docker_image.contains(keyword),
                    Benchmark.docker_tag.contains(keyword),
                    Benchmark.description.contains(keyword)
                ))

        return results


# --------------------------------------------------------------------
# SITE model

class Site(HasReports, HasCreationDetails, PkModel):
    """The Site class represents a location where a benchmark can be executed.

    This generally refers to the different virtual machine providers.
    """
    name = Column(Text, unique=True, nullable=False)
    address = Column(Text, nullable=False)
    description = Column(Text, nullable=True, default="")
    flavors = relationship("Flavor", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Get a human-readable representation string of the site.

        Returns:
            str: A human-readable representation string of the site.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    @classmethod
    def query_with(cls, terms):
        """Query all sites containing all keywords in the columns.

        Args:
            terms (List[str]): A list of all keywords that need to be matched.
        Returns:
            List[Result]: A list containing all matching query sites in the
            database.
        """
        results = cls.query
        for keyword in terms:
            results = results.filter(
                or_(
                    Site.name.contains(keyword),
                    Site.address.contains(keyword),
                    Site.description.contains(keyword)
                ))

        return results


# --------------------------------------------------------------------
# FLAVOR model

class Flavor(HasReports, HasCreationDetails, PkModel):
    """The Flavor class represents a flavor of virtual machines available
    for usage on a Site.

    Flavours can be pre-existing options filled in by administrators or a
    custom configuration by the user.
    """
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True, default="")
    site_id = Column(ForeignKey('site.id'), nullable=False)

    @declared_attr
    def __table_args__(cls):
        mixin_indexes = list((HasCreationDetails.__table_args__))
        mixin_indexes.extend([
            UniqueConstraint('site_id', 'name')
        ])
        return tuple(mixin_indexes)

    def __repr__(self) -> str:
        """Get a human-readable representation string of the site flavor.

        Returns:
            str: A human-readable representation string of the site flavor.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)


# --------------------------------------------------------------------
# RESULT model

class Result(HasReports, HasTags, HasCreationDetails, PkModel):
    """The Result class represents a single benchmark result and its contents.

    They carry the JSON data output by the ran benchmarks.
    """
    json = Column(JSONB, nullable=False)

    benchmark_id = Column(ForeignKey('benchmark.id'), nullable=False)
    benchmark = relationship(Benchmark, backref=backref(
        "results", cascade="all, delete-orphan"
    ))
    docker_image = association_proxy('benchmark', 'docker_image')
    docker_tag = association_proxy('benchmark', 'docker_tag')

    site_id = Column(ForeignKey('site.id'), nullable=False)
    site = relationship(Site, backref=backref(
        "results", cascade="all, delete-orphan"
    ))
    site_name = association_proxy('site', 'name')

    flavor_id = Column(ForeignKey('flavor.id'), nullable=False)
    flavor = relationship(Flavor, backref=backref(
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
    def query_with(cls, terms):
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
                or_(
                    Result.docker_image.contains(keyword),
                    Result.docker_tag.contains(keyword),
                    Result.site_name.contains(keyword),
                    Result.flavor_name.contains(keyword),
                    Result.tag_names == keyword
                ))

        return results
