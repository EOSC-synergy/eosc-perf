"""Site models."""
from backend.database import PkModel
from backend.models import Report, ReportAssociation
from backend.models import User
from sqlalchemy import Column, ForeignKey, Text, UniqueConstraint, or_
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

__all__ = [
    'Report', 'User',
    'Site', 'SiteReportAssociation',
    'Flavor', 'FlavorReportAssociation'
]


class SiteReportAssociation(ReportAssociation):
    __tablename__ = None
    __mapper_args__ = {"polymorphic_identity": "site_report"}
    parent = relationship("Site", uselist=False,
                          back_populates="report_association")


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


class FlavorReportAssociation(ReportAssociation):
    __tablename__ = None
    __mapper_args__ = {"polymorphic_identity": "flavor_report"}
    parent = relationship("Flavor", uselist=False,
                          back_populates="report_association")


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
