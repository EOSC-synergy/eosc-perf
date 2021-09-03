"""Reports module with mixin that provides a generic association
using a single target table and a single association table,
referred to by all parent tables.  The association table
contains a "discriminator" column which determines what type of
parent object associates to each particular row in the association
table.

SQLAlchemy's single-table-inheritance feature is used to target 
different association types.
"""
import enum
from datetime import datetime as dt

from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import DateTime

from ..core import PkModel
from . import HasUploadDatetime
from .user import HasUploader


class ResourceStatus(enum.Enum):
    on_review = 1
    approved = 2


class Report(HasUploadDatetime, HasUploader, PkModel):
    """The Report model represents an automated request for review. For
    example the creation of items which need to be approved before 
    activated in the database or the notification that a new claim is
    created.  

    **Properties**:
    """
    _association_id = Column(ForeignKey("report_association.id"))
    _association = relationship("ReportAssociation", back_populates="reports")

    #: (Resource) Resource the report refers to (Benchmark, Result, etc.)
    resource = association_proxy("_association", "parent")

    #: (Read_only) Resource discriminator
    resource_type = association_proxy("_association", "discriminator")

    #: (Read_only) Resource unique identification
    resource_id = association_proxy("_association", "parent.id")

    #: (ISO8601, required) Datetime when the report was processed
    processed_datetime = Column(DateTime, nullable=True)

    def __init__(self, **properties):
        """Model initialization"""
        super().__init__(**properties)

    def __repr__(self):
        """Human-readable representation string"""
        return "{} {}".format(self.__class__.__name__, self.report_type)

    def approve(self):
        """Acknowledge report and change resource status to accepted."""
        if self.resource.status != ResourceStatus.on_review:
            raise RuntimeError("Report already processed")
        self.processed_datetime = dt.datetime.now()
        self.resource.status = ResourceStatus.approved


class ReportAssociation(PkModel):
    """Associates a collection of Report objects with a particular parent.
    """
    __tablename__ = "report_association"

    #: (String) Refers to the type of model the report is associated
    discriminator = Column(String)
    __mapper_args__ = {"polymorphic_on": discriminator}

    #: ([Report]) List of reports related to the model instance
    reports = relationship(
        "Report", cascade="all, delete-orphan",
        back_populates="_association"
    )


class HasReports(object):
    """HasReports mixin, creates a new report_association table for each parent.
    """

    #: (ItemStatus) Status of the resource
    status = Column(Enum(ResourceStatus), default=ResourceStatus.on_review)

    @declared_attr
    def _report_association_id(cls):
        return Column(ForeignKey("report_association.id"), nullable=False)

    @declared_attr
    def _report_association_class(cls):
        discriminator = cls.__name__.lower()
        return type(
            f"{cls.__name__}ReportAssociation",
            (ReportAssociation,),
            dict(
                __tablename__=None,
                __mapper_args__={"polymorphic_identity": discriminator},
            ),
        )

    @declared_attr
    def _report_association(cls):
        return relationship(
            cls._report_association_class, single_parent=True,
            cascade="all, delete-orphan",
            backref=backref("parent", uselist=False)
        )

    @declared_attr
    def reports(cls):
        """([Report]) List of reports related to the model instance"""
        association = cls._report_association_class
        return association_proxy(
            "_report_association", "reports",
            creator=lambda reports: association(reports=reports),
        )
