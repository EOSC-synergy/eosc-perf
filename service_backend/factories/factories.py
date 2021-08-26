"""Factories module to define the main model factories"""
import uuid

from backend import models
from factory import (LazyFunction, SelfAttribute, Sequence, SubFactory,
                     post_generation)
from factory.alchemy import SQLAlchemyModelFactory

from .core import BaseMeta, fdt


class DBUser(SQLAlchemyModelFactory):
    """User factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.User
        sqlalchemy_get_or_create = ('email',)

    sub = Sequence(lambda n: f"user{n}")
    iss = "https://aai-dev.egi.eu/oidc"
    email = Sequence(lambda n: f"user{n}@example.com")


class DBReport(SQLAlchemyModelFactory):
    """Report factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.Report

    id = LazyFunction(uuid.uuid4)
    upload_datetime = fdt.fuzz()
    verdict = None
    message = Sequence(lambda n: f"Report message {n}")
    uploader = SubFactory(DBUser)


class DBBenchmark(SQLAlchemyModelFactory):
    """Benchmark factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.Benchmark
        sqlalchemy_get_or_create = ('docker_image', 'docker_tag')

    id = LazyFunction(uuid.uuid4)
    upload_datetime = fdt.fuzz()
    docker_image = Sequence(lambda n: f"b{n}")
    docker_tag = "latest"
    description = ""
    json_schema = {}
    upload_datetime = fdt.fuzz()
    uploader = SubFactory(DBUser)

    @post_generation
    def upload_verdict(self, create, verdict, **kwargs):
        if verdict != None:
            self.reports[0].verdict = verdict


class DBSite(SQLAlchemyModelFactory):
    """Site factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.Site
        sqlalchemy_get_or_create = ('name',)

    id = LazyFunction(uuid.uuid4)
    upload_datetime = fdt.fuzz()
    name = Sequence(lambda n: f"site{n}")
    address = Sequence(lambda n: f"address{n}")
    description = "Text"
    upload_datetime = fdt.fuzz()
    uploader = SubFactory(DBUser)

    @post_generation
    def upload_verdict(self, create, verdict, **kwargs):
        if verdict != None:
            self.reports[0].verdict = verdict


class DBFlavor(SQLAlchemyModelFactory):
    """Flavor factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.Flavor
        sqlalchemy_get_or_create = ('name', 'site_id')

    id = LazyFunction(uuid.uuid4)
    upload_datetime = fdt.fuzz()
    name = Sequence(lambda n: f"flavor{n}")
    description = "Text"
    site_id = LazyFunction(lambda: DBSite().id)
    upload_datetime = fdt.fuzz()
    uploader = SubFactory(DBUser)

    @post_generation
    def upload_verdict(self, create, verdict, **kwargs):
        if verdict != None:
            self.reports[0].verdict = verdict


class DBTag(SQLAlchemyModelFactory):
    """Tag factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.Tag
        sqlalchemy_get_or_create = ('name',)

    id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: f"tag{n}")
    description = "Description"


class DBResult(SQLAlchemyModelFactory):
    """Result factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.Result
        sqlalchemy_get_or_create = ('id',)

    id = LazyFunction(uuid.uuid4)
    upload_datetime = fdt.fuzz()
    execution_datetime = fdt.fuzz()
    json = Sequence(lambda n: {'name': f"report_{n}"})
    benchmark = SubFactory(DBBenchmark)
    site = SubFactory(DBSite)
    flavor = SubFactory(DBFlavor, site_id=SelfAttribute('..site.id'))
    upload_datetime = fdt.fuzz()
    uploader = SubFactory(DBUser)

    @post_generation
    def tags(self, create, names, **kwargs):
        names = names if names is not None else []
        for name in names:
            tag = DBTag(name=name, **kwargs)
            self.tags.append(tag)

    @post_generation
    def reports(self, create, reports, **kwargs):
        if reports:
            for kwargs in reports:
                report = DBReport(
                    _association_id=self._report_association_id,
                    **kwargs
                )
                self._report_association.reports.append(report)
