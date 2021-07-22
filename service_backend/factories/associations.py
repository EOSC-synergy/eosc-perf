"""Factories module to fill required associations"""
import uuid

from backend.models import associations
from factory import LazyFunction, post_generation
from factory.alchemy import SQLAlchemyModelFactory

from factories import BaseMeta
from factories import factories


class ReportBase(SQLAlchemyModelFactory):
    """Report association factory base."""
    id = LazyFunction(uuid.uuid4)
    parent = None

    @post_generation
    def reports(self, create, ids, **kwargs):
        ids = ids if ids is not None else [uuid.uuid4()]
        for id in ids:
            report = factories.DBReport(id=id, association_id=self.id, **kwargs)
            self.reports.append(report)


class DBBenchmarkReport(ReportBase):
    """Benchmark Report association factory."""
    class Meta(BaseMeta):
        model = associations.BenchmarkReport


class DBResultReport(ReportBase):
    """Result Report association factory."""
    class Meta(BaseMeta):
        model = associations.ResultReport


class DBSiteReport(ReportBase):
    """Site Report association factory."""
    class Meta(BaseMeta):
        model = associations.SiteReport


class DBFlavorReport(ReportBase):
    """Flavor Report association factory."""
    class Meta(BaseMeta):
        model = associations.FlavorReport
