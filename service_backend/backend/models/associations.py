"""Models module for association definitions."""
from backend.database import PkModel
from sqlalchemy import Column, String
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
