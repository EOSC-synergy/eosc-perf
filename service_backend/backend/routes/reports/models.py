"""Report models."""
from datetime import datetime

from backend.database import PkModel
from backend.models import User
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey,
                        ForeignKeyConstraint, String, Text)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship


__all__ = [
    'Report', 'User', 'ReportAssociation'
]


class ReportAssociation(PkModel):
    discriminator = Column(String)  # Refers to the type of parent
    reports = relationship(
        "Report",
        cascade="all, delete-orphan",
        back_populates="association"
    )
    __mapper_args__ = {"polymorphic_on": discriminator}


class Report(PkModel):
    """The Report class represents an automated or an user’s report.

    Reports are automated if used to submit new benchmarks or sites, in which
    case the report will need to be approved before the associated site or
    benchmark becomes visible.

    Reports can also be manually generated if users choose to report a result
    from their search results if they suspect it may be falsified or incorrect.
    """
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    verdict = Column(Boolean, nullable=True)
    message = Column(Text, nullable=True)

    association_id = Column(ForeignKey("report_association.id"))
    association = relationship("ReportAssociation", back_populates="reports")

    resource = association_proxy("association", "parent")
    resource_type = association_proxy("association", "discriminator")
    resource_id = association_proxy("association", "parent.id")

    uploader_iss = Column(Text, nullable=False)
    uploader_sub = Column(Text, nullable=False)
    uploader = relationship("User")
    __table_args__ = (ForeignKeyConstraint(['uploader_iss', 'uploader_sub'],
                                           ['user.iss', 'user.sub']),
                      {})

    def __repr__(self):
        return f"{self.__class__.__name__} {self.id}"
