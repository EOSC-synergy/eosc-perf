"""Result models."""
from datetime import datetime

from backend.benchmarks.models import Benchmark
from backend.database import PkModel, Table
from backend.reports.models import Report, ReportAssociation
from backend.sites.models import Flavor, Site
from backend.tags.models import Tag
from backend.users.models import User
from sqlalchemy import (Column, DateTime, ForeignKey, ForeignKeyConstraint,
                        PrimaryKeyConstraint, Text, or_)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

tag_association = Table(
    'result_tags',
    Column('result_id', ForeignKey('result.id')),
    Column('tag_id', ForeignKey('tag.id')),
    PrimaryKeyConstraint('result_id', 'tag_id')
)


class ResultReportAssociation(ReportAssociation):
    __tablename__ = None
    __mapper_args__ = {"polymorphic_identity": "result_report"}
    parent = relationship("Result", uselist=False,
                          back_populates="report_association")


class Result(PkModel):
    """The Result class represents a single benchmark result and its contents.

    They carry the JSON data output by the ran benchmarks.
    """

    upload_date = Column(DateTime, nullable=False, default=datetime.now)
    json = Column(JSONB, nullable=False)
    tags = relationship(Tag, secondary=tag_association)
    tag_names = association_proxy('tags', 'name')

    benchmark_id = Column(ForeignKey('benchmark.id'), nullable=False)
    benchmark = relationship(Benchmark)
    docker_image = association_proxy('benchmark', 'docker_image')
    docker_tag = association_proxy('benchmark', 'docker_tag')

    site_id = Column(ForeignKey('site.id'), nullable=False)
    site = relationship(Site)
    site_name = association_proxy('site', 'name')

    flavor_id = Column(ForeignKey('flavor.id'), nullable=False)
    flavor = relationship(Flavor)
    flavor_name = association_proxy('flavor', 'name')

    uploader_iss = Column(Text, nullable=False)
    uploader_sub = Column(Text, nullable=False)
    uploader = relationship(User)

    report_association_id = Column(ForeignKey("report_association.id"))
    report_association = relationship(
        ResultReportAssociation, single_parent=True,
        cascade="all, delete-orphan",
        back_populates="parent")
    reports = association_proxy(
        "report_association", "reports",
        creator=lambda reports: ResultReportAssociation(reports=reports))
    verdicts = association_proxy('reports', 'verdict')

    @ hybrid_property
    def hidden(self):
        return not all(self.verdicts)

    __table_args__ = (ForeignKeyConstraint(['uploader_iss', 'uploader_sub'],
                                           ['user.iss', 'user.sub']),
                      {})

    def __repr__(self) -> str:
        """Get a human-readable representation string of the result.

        Returns:
            str: A human-readable representation string of the result.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.id)

    @ classmethod
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
                    # TODO: Result.json.contains(keyword),
                    Result.docker_image.contains(keyword),
                    Result.docker_tag.contains(keyword),
                    Result.site_name.contains(keyword),
                    Result.flavor_name.contains(keyword),
                    Result.tag_names == keyword
                ))

        return results
