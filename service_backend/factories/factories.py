"""Factories module to define the main model factories"""
import uuid

from backend.models import models
from factory import (LazyFunction, SelfAttribute, Sequence, SubFactory,
                     post_generation)
from factory.alchemy import SQLAlchemyModelFactory

from factories import BaseMeta, fdt


class DBUser(SQLAlchemyModelFactory):
    """User factory."""
    class Meta(BaseMeta):
        model = models.User
        sqlalchemy_get_or_create = ('email',)

    sub = Sequence(lambda n: f"user{n}")
    iss = "egi.com"
    email = Sequence(lambda n: f"user{n}@example.com")


class DBReport(SQLAlchemyModelFactory):
    """Report factory."""
    class Meta(BaseMeta):
        model = models.Report

    id = LazyFunction(uuid.uuid4)
    created_at = fdt.fuzz()
    verdict = None
    message = Sequence(lambda n: f"Report message {n}")
    created_by = SubFactory(DBUser)


class DBBenchmark(SQLAlchemyModelFactory):
    """Benchmark factory."""
    class Meta(BaseMeta):
        model = models.Benchmark
        sqlalchemy_get_or_create = ('docker_image', 'docker_tag')

    id = LazyFunction(uuid.uuid4)
    created_at = fdt.fuzz()
    docker_image = Sequence(lambda n: f"b{n}")
    docker_tag = "latest"
    description = ""
    json_schema = {}
    created_at = fdt.fuzz()
    created_by = SubFactory(DBUser)

    @post_generation
    def creation_report(self, create, _, **kwargs):
        if self.reports == []:
            creation_report = DBReport(
                association_id=self.report_association_id,
                created_by__email=self.created_by.email,
                created_at=self.created_at, **kwargs
            )
            self.report_association.reports.append(creation_report)


class DBSite(SQLAlchemyModelFactory):
    """Site factory."""
    class Meta(BaseMeta):
        model = models.Site
        sqlalchemy_get_or_create = ('name',)

    id = LazyFunction(uuid.uuid4)
    created_at = fdt.fuzz()
    name = Sequence(lambda n: f"site{n}")
    address = Sequence(lambda n: f"address{n}")
    description = "Text"
    created_at = fdt.fuzz()
    created_by = SubFactory(DBUser)

    @post_generation
    def creation_report(self, create, _, **kwargs):
        if self.reports == []:
            creation_report = DBReport(
                association_id=self.report_association_id,
                created_by__email=self.created_by.email,
                created_at=self.created_at, **kwargs
            )
            self.report_association.reports.append(creation_report)


class DBFlavor(SQLAlchemyModelFactory):
    """Flavor factory."""
    class Meta(BaseMeta):
        model = models.Flavor
        sqlalchemy_get_or_create = ('name', 'site_id')

    id = LazyFunction(uuid.uuid4)
    created_at = fdt.fuzz()
    name = Sequence(lambda n: f"flavor{n}")
    description = "Text"
    site_id = LazyFunction(lambda: DBSite().id)
    created_at = fdt.fuzz()
    created_by = SubFactory(DBUser)

    @post_generation
    def creation_report(self, create, _, **kwargs):
        if self.reports == []:
            creation_report = DBReport(
                association_id=self.report_association_id,
                created_by__email=self.created_by.email,
                created_at=self.created_at, **kwargs
            )
            self.report_association.reports.append(creation_report)


class DBTag(SQLAlchemyModelFactory):
    """Tag factory."""
    class Meta(BaseMeta):
        model = models.Tag
        sqlalchemy_get_or_create = ('name',)

    id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: f"tag{n}")
    description = "Description"


class DBResult(SQLAlchemyModelFactory):
    """Result factory."""
    class Meta(BaseMeta):
        model = models.Result
        sqlalchemy_get_or_create = ('id',)

    id = LazyFunction(uuid.uuid4)
    created_at = fdt.fuzz()
    executed_at = fdt.fuzz()
    json = Sequence(lambda n: {'name': f"report_{n}"})
    benchmark = SubFactory(DBBenchmark)
    site = SubFactory(DBSite)
    flavor = SubFactory(DBFlavor, site_id=SelfAttribute('..site.id'))
    created_at = fdt.fuzz()
    created_by = SubFactory(DBUser)

    @post_generation
    def tags(self, create, names, **kwargs):
        names = names if names is not None else []
        for name in names:
            tag = DBTag(name=name, **kwargs)
            self.tags.append(tag)

    @post_generation
    def reports(self, create, reports, **kwargs):
        reports = reports if reports is not None else []
        for kwargs in reports:
            report = DBReport(
                association_id=self.report_association_id,
                **kwargs
            )
            self.report_association.reports.append(report)
