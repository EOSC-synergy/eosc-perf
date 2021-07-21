"""Factories to help in tests."""
import uuid
from datetime import datetime

from backend.models import Benchmark, BenchmarkReportAssociation
from backend.models import Report
from backend.routes.results.models import Result, ResultReportAssociation
from backend.models import (Flavor, FlavorReportAssociation, Site,
                            SiteReportAssociation)
from backend.models import Tag
from backend.models import User
from factory import (LazyFunction, SelfAttribute, Sequence, SubFactory,
                     post_generation)
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyNaiveDateTime

from . import conftest

fdt = FuzzyNaiveDateTime(datetime(2000, 1, 1))


class BaseMeta:
    """Factory configuration."""
    # Use the not-so-global scoped_session
    # Warning: DO NOT USE common.Session()!
    sqlalchemy_session = conftest.Session


class TagFactory(SQLAlchemyModelFactory):
    """Tag factory."""
    class Meta(BaseMeta):
        model = Tag
        sqlalchemy_get_or_create = ('name',)

    id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: f"tag{n}")
    description = "Description"


class UserFactory(SQLAlchemyModelFactory):
    """User factory."""
    class Meta(BaseMeta):
        model = User
        sqlalchemy_get_or_create = ('sub', 'iss')

    sub = Sequence(lambda n: f"user{n}")
    iss = "egi.com"
    email = Sequence(lambda n: f"user{n}@example.com")


class ReportFactory(SQLAlchemyModelFactory):
    """Report factory."""
    class Meta(BaseMeta):
        model = Report

    id = LazyFunction(uuid.uuid4)
    creation_date = fdt.fuzz()
    verdict = True
    message = Sequence(lambda n: f"Report message {n}")
    uploader = SubFactory(UserFactory)


class ReportAssociationFactory(SQLAlchemyModelFactory):
    """Report association factory base."""
    id = LazyFunction(uuid.uuid4)
    parent = None

    @post_generation
    def reports(self, create, ids, **kwargs):
        ids = ids if ids is not None else [uuid.uuid4()]
        for id in ids:
            report = ReportFactory(id=id, association_id=self.id, **kwargs)
            self.reports.append(report)


class BenchmarkReportAssociationFactory(ReportAssociationFactory):
    """Benchmark Report association factory."""
    class Meta(BaseMeta):
        model = BenchmarkReportAssociation


class ResultReportAssociationFactory(ReportAssociationFactory):
    """Result Report association factory."""
    class Meta(BaseMeta):
        model = ResultReportAssociation


class SiteReportAssociationFactory(ReportAssociationFactory):
    """Site Report association factory."""
    class Meta(BaseMeta):
        model = SiteReportAssociation


class FlavorReportAssociationFactory(ReportAssociationFactory):
    """Flavor Report association factory."""
    class Meta(BaseMeta):
        model = FlavorReportAssociation


class BenchmarkFactory(SQLAlchemyModelFactory):
    """Benchmark factory."""
    class Meta(BaseMeta):
        model = Benchmark
        sqlalchemy_get_or_create = ('docker_image', 'docker_tag')

    id = LazyFunction(uuid.uuid4)
    docker_image = Sequence(lambda n: f"b{n}")
    docker_tag = "latest"
    description = ""
    json_template = {}
    report_association = SubFactory(BenchmarkReportAssociationFactory)


class SiteFactory(SQLAlchemyModelFactory):
    """Site factory."""
    class Meta(BaseMeta):
        model = Site
        sqlalchemy_get_or_create = ('name',)

    id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: f"site{n}")
    address = Sequence(lambda n: f"address{n}")
    description = "Text"
    report_association = SubFactory(SiteReportAssociationFactory)

    @post_generation
    def flavors(self, create, names, **kwargs):
        if names:
            [FlavorFactory(site_id=self.id, name=n, **kwargs) for n in names]


class FlavorFactory(SQLAlchemyModelFactory):
    """Flavor factory."""
    class Meta(BaseMeta):
        model = Flavor
        sqlalchemy_get_or_create = ('name', 'site_id')

    id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: f"flavor{n}")
    description = "Text"
    site_id = LazyFunction(lambda: SiteFactory().id)
    report_association = SubFactory(FlavorReportAssociationFactory)


class ResultFactory(SQLAlchemyModelFactory):
    """Result factory."""
    class Meta(BaseMeta):
        model = Result

    id = LazyFunction(uuid.uuid4)
    json = Sequence(lambda n: {'name': f"report_{n}"})
    uploader = SubFactory(UserFactory)
    benchmark = SubFactory(BenchmarkFactory)
    site = SubFactory(SiteFactory)
    flavor = SubFactory(FlavorFactory, site_id=SelfAttribute('..site.id'))
    report_association = SubFactory(ResultReportAssociationFactory)

    @post_generation
    def tags(self, create, kws, **kwargs):
        if kws:
            self.tags = [TagFactory(**kw) for kw in kws]
        else:
            self.tags = []
