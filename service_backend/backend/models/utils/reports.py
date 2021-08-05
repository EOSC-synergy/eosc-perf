"""Reports module with mixin that provides a generic association
using a single target table and a single association table,
referred to by all parent tables.  The association table
contains a "discriminator" column which determines what type of
parent object associates to each particular row in the association
table.

SQLAlchemy's single-table-inheritance feature is used
to target different association types.
"""
from sqlalchemy import Boolean, Column, ForeignKey, String, Text, select
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, column_property, relationship

from .. import PkModel
from . import utils


class ReportAssociation(PkModel):
    """Associates a collection of Report objects with a particular parent.
    """
    __tablename__ = "report_association"
    discriminator = Column(String)  # Refers to the type of parent
    reports = relationship(
        "Report", cascade="all, delete-orphan",
        back_populates="association"
    )
    __mapper_args__ = {"polymorphic_on": discriminator}


class Report(utils.HasCreationDetails, PkModel):
    """The Report class represents an automated or an user’s report.

    Reports are automated if used to submit new benchmarks or sites, in which
    case the report will need to be approved before the associated site or
    benchmark becomes visible.

    Reports can also be manually generated if users choose to report a result
    from their search results if they suspect it may be falsified or incorrect.
    """
    verdict = Column(Boolean, nullable=True)
    message = Column(Text, nullable=True)

    association_id = Column(ForeignKey("report_association.id"))
    association = relationship(ReportAssociation, back_populates="reports")

    resource = association_proxy("association", "parent")
    resource_type = association_proxy("association", "discriminator")
    resource_id = association_proxy("association", "parent.id")

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id}"


class HasReports(object):
    """Mixin that creates a relationship to the report_association table for
    each parent.
    """
    __abstract__ = True

    def __init__(self, reports=[], **kwargs):
        """Overwrite create to add reports=[] if not defined."""
        super().__init__(reports=reports, **kwargs)

    @declared_attr
    def report_association_id(cls):
        return Column(ForeignKey("report_association.id"), nullable=False)

    @declared_attr
    def report_association(cls):
        name = cls.__name__
        discriminator = name.lower()

        assoc_cls = type(
            f"{name}ReportAssociation",
            (ReportAssociation,),
            dict(
                __tablename__=None,
                __mapper_args__={"polymorphic_identity": discriminator},
            ),
        )

        cls.reports = association_proxy(
            "report_association",
            "reports",
            creator=lambda reports: assoc_cls(reports=reports),
        )
        return relationship(
            assoc_cls, single_parent=True,
            cascade="all, delete-orphan",
            backref=backref("parent", uselist=False)
        )

    @declared_attr
    def reports_unresolved(cls):
        return column_property(
            select([Report.id]).
            where(Report.association_id == cls.report_association_id).
            where(Report.verdict == False).
            scalar_subquery()
        )

    @hybrid_property
    def hidden(self):
        return self.reports_unresolved != None

    @hidden.expression
    def hidden(cls):
        return cls.id.in_(
            select([cls.id]).where(cls.reports_unresolved != None)
        )
