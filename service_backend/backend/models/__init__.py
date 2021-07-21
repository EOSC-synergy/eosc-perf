"""Backend package for models definition."""
from datetime import datetime as dt

from backend.database import BaseModel, PkModel
from backend.extensions import auth
from flaat import tokentools
from flask_smorest import abort
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey,
                        ForeignKeyConstraint, Text, UniqueConstraint, or_)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .associations import (BenchmarkReportAssociation, FlavorReportAssociation,
                           ReportAssociation, SiteReportAssociation)


class User(BaseModel):
    """A user of the app."""

    sub = Column(Text, primary_key=True, nullable=False)
    iss = Column(Text, primary_key=True, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=dt.utcnow)

    __table_args__ = (
        UniqueConstraint('sub', 'iss'),
    )

    def __repr__(self) -> str:
        """Get a human-readable representation string of the user.

        Returns:
            str: A human-readable representation string of the user.
        """
        return "<{} {}>".format(self.__class__.__name__, self.email)

    @classmethod
    def create(cls, token):
        token_info = tokentools.get_accesstoken_info(token)
        user_info = auth.get_info_from_introspection_endpoints(token)

        if not user_info:
            abort(500, messages={'introspection endpoint': "No user info"})

        elif 'email' not in user_info:
            abort(422, messages={'token': "No scope for email"})

        return super().create(
            sub=token_info['body']['sub'],
            iss=token_info['body']['iss'],
            email=user_info['email']
        )

    @classmethod
    def get(cls, sub=None, iss=None, token=None):

        if not sub and not iss and not token:
            raise TypeError("Missing sub & iss or token")

        elif not sub and not iss:
            token_info = tokentools.get_accesstoken_info(token)
            sub = token_info['body']['sub'],
            iss = token_info['body']['iss'],

        user = cls.query.get((sub, iss))
        if user:
            return user
        else:
            abort(404, messages={'user': "Not registered"})

    @classmethod
    def query_emails_with(cls, terms):
        results = cls.query
        for keyword in terms:
            results = results.filter(
                User.email.contains(keyword)
            )
        return results

    def update_info(self, token):
        user_info = auth.get_info_from_introspection_endpoints(token)
        return super().update(
            email=user_info['email']
        )


class Report(PkModel):
    """The Report class represents an automated or an user’s report.

    Reports are automated if used to submit new benchmarks or sites, in which
    case the report will need to be approved before the associated site or
    benchmark becomes visible.

    Reports can also be manually generated if users choose to report a result
    from their search results if they suspect it may be falsified or incorrect.
    """
    creation_date = Column(DateTime, nullable=False, default=dt.now)
    verdict = Column(Boolean, nullable=True)
    message = Column(Text, nullable=True)

    association_id = Column(ForeignKey("report_association.id"))
    association = relationship(ReportAssociation, back_populates="reports")

    resource = association_proxy("association", "parent")
    resource_type = association_proxy("association", "discriminator")
    resource_id = association_proxy("association", "parent.id")

    uploader_iss = Column(Text, nullable=False)
    uploader_sub = Column(Text, nullable=False)
    uploader = relationship(User)
    __table_args__ = (ForeignKeyConstraint(['uploader_iss', 'uploader_sub'],
                                           ['user.iss', 'user.sub']),
                      {})

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id}"


class Benchmark(PkModel):
    """The benchmark class represents a single type of benchmark that was run.

    Benchmarks are tied down to a specific docker image version to avoid
    confusion and misleading comparisons in case the benchmark images change
    their metrics or scoring scale from version to version.
    """
    docker_image = Column(Text, nullable=False)
    docker_tag = Column(Text, nullable=False)
    description = Column(Text, default="")
    json_template = Column(JSON, default={})

    report_association_id = Column(ForeignKey("report_association.id"))
    report_association = relationship(
        BenchmarkReportAssociation, single_parent=True,
        cascade="all, delete-orphan",
        back_populates="parent")
    reports = association_proxy(
        "report_association", "reports",
        creator=lambda reports: BenchmarkReportAssociation(reports=reports))
    verdict = association_proxy('reports', 'verdict')

    @hybrid_property
    def hidden(self):
        return not self.verdict

    __table_args__ = (
        UniqueConstraint('docker_image', 'docker_tag'),
    )

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


class Site(PkModel):
    """The Site class represents a location where a benchmark can be executed.

    This generally refers to the different virtual machine providers.
    """

    name = Column(Text, unique=True, nullable=False)
    address = Column(Text, nullable=False)
    description = Column(Text, nullable=True, default="")
    flavors = relationship("Flavor", cascade="all, delete-orphan")

    report_association_id = Column(ForeignKey("report_association.id"))
    report_association = relationship(
        SiteReportAssociation, single_parent=True,
        cascade="all, delete-orphan",
        back_populates="parent")
    reports = association_proxy(
        "report_association", "reports",
        creator=lambda reports: SiteReportAssociation(reports=reports))
    verdicts = association_proxy('reports', 'verdict')

    @hybrid_property
    def hidden(self):
        return not self.verdict

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


class Flavor(PkModel):
    """The Flavor class represents a flavor of virtual machines available
    for usage on a Site.

    Flavours can be pre-existing options filled in by administrators or a
    custom configuration by the user.
    """

    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True, default="")
    site_id = Column(ForeignKey('site.id'), nullable=False)
    verdict = association_proxy('reports', 'verdict')

    report_association_id = Column(ForeignKey("report_association.id"))
    report_association = relationship(
        FlavorReportAssociation, single_parent=True,
        cascade="all, delete-orphan",
        back_populates="parent")
    reports = association_proxy(
        "report_association", "reports",
        creator=lambda reports: FlavorReportAssociation(reports=reports))
    verdicts = association_proxy('reports', 'verdict')

    @hybrid_property
    def hidden(self):
        return not self.verdict

    __table_args__ = (
        UniqueConstraint('site_id', 'name'),
    )

    def __repr__(self) -> str:
        """Get a human-readable representation string of the site flavor.

        Returns:
            str: A human-readable representation string of the site flavor.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)


class Tag(PkModel):
    """The Tag class represents a user-created label that can be used for
    filtering a list of results.

    These are entirely created by users and may not necessarily be related to
    any benchmark output data. These may be used to indicate if, for example, a
    benchmark is used to measure CPU or GPU performance, since some benchmarks
    may be used to test both.
    """

    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False, default="")

    def __repr__(self) -> str:
        """Get a human-readable representation string of the tag.

        Returns:
            str: A human-readable representation string of the tag.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    @classmethod
    def query_with(cls, terms):
        """Query all tags containing all keywords.

        Args:
            terms (List[str]): A list of all keywords to match on the search.
        Returns:
            List[Tag]: A list containing all matching tags in the database.
        """
        results = cls.query
        for keyword in terms:
            results = results.filter(
                or_(
                    Tag.name.contains(keyword),
                    Tag.description.contains(keyword)
                ))

        return results
