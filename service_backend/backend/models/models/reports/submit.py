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

from backend.models.models.user import HasUploader
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship

from ...core import PkModel


class Submit(PkModel):
    """The Submit model represents an automated request for review.
    For example the creation of items which need to be approved before
    activated in the database or the notification that a new claim is
    created.

    **Properties**:
    """
    #: (Resource) Resource the submit is linked to
    resource = NotImplementedError()  # Implemented at NeedsApprove

    #: (String) Refers to the type report
    resource_type = Column(String, nullable=False)

    #: (Read_only) Resource unique identification
    resource_id = association_proxy("resource", "id")

    #: (Read_only) Upload datetime of the model instance
    # upload_datetime = association_proxy("resource", "upload_datetime")
    upload_datetime = Column(DateTime, nullable=False, default=dt.now)

    # Polymorphism related to the resource the submit is linked
    __mapper_args__ = {
        'polymorphic_on': resource_type,
        # 'with_polymorphic': '*'
    }

    def __init__(self, **properties):
        """Model initialization"""
        super().__init__(**properties)

    def __repr__(self):
        """Human-readable representation string"""
        return "{}({}): {}".format(
            self.__class__.__name__,
            self.resource_type,
            self.id
        )


class ResourceStatus(enum.Enum):
    on_review = 1
    approved = 2


class NeedsApprove(HasUploader):
    """Creates a new submit report together with the new resource.
    """
    __abstract__ = True

    #: (ItemStatus) Status of the resource
    status = Column(Enum(ResourceStatus), default=ResourceStatus.on_review)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__class__._submit_report_class(resource=self)

    @declared_attr
    def _submit_report_id(cls):
        return Column(ForeignKey('submit.id'))

    @declared_attr
    def _submit_report_class(cls):
        return type(
            f"{cls.__name__}SubmitReport", (Submit,),
            dict(
                __mapper_args__={
                    'polymorphic_identity': cls.__name__.lower(),
                    'polymorphic_load': 'inline'
                },
            ),
        )

    @declared_attr
    def submit_report(cls):
        """(Report) Submit report related to the model instance"""
        return relationship(
            cls._submit_report_class, cascade="all, delete",
            backref=backref("resource", uselist=False),
        )

    def approve(self):
        """Removes the submit report once approved."""
        if self.status == ResourceStatus.approved:
            raise RuntimeError("Resource already approved")
        else:
            self.submit_report.delete()
            self.submit_report = None
            self.status = ResourceStatus.approved

    def reject(self):
        """Removes the element and submit report."""
        if self.status == ResourceStatus.approved:
            raise RuntimeError("Resource already approved")
        else:
            # self.submit_report.delete() # Cascades
            # self.submit_report = None
            self.delete()
