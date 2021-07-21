"""Models module for association definitions."""
from backend.database import BaseModel, PkModel
from sqlalchemy import Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship


class ReportAssociation(PkModel):
    discriminator = Column(String)  # Refers to the type of parent
    reports = relationship(
        "Report", cascade="all, delete-orphan",
        back_populates="association"
    )
    __mapper_args__ = {"polymorphic_on": discriminator}


class BenchmarkReportAssociation(ReportAssociation):
    __tablename__ = None
    parent = relationship(
        "Benchmark", uselist=False,
        back_populates="report_association"
    )
    __mapper_args__ = {"polymorphic_identity": "benchmark_report"}


class SiteReportAssociation(ReportAssociation):
    __tablename__ = None
    parent = relationship(
        "Site", uselist=False,
        back_populates="report_association"
    )
    __mapper_args__ = {"polymorphic_identity": "site_report"}


class FlavorReportAssociation(ReportAssociation):
    __tablename__ = None
    parent = relationship(
        "Flavor", uselist=False,
        back_populates="report_association"
    )
    __mapper_args__ = {"polymorphic_identity": "flavor_report"}


class ResultReportAssociation(ReportAssociation):
    __tablename__ = None
    parent = relationship(
        "Result", uselist=False,
        back_populates="report_association"
    )
    __mapper_args__ = {"polymorphic_identity": "result_report"}


class ResultTagsAssociation(BaseModel):
    result_id = Column(ForeignKey('result.id'), primary_key=True)
    tag_id = Column(ForeignKey('tag.id'), primary_key=True)
    __table_args__ = (UniqueConstraint('result_id', 'tag_id'),)
