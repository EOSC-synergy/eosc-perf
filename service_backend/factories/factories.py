"""Factories module to define the main model factories"""
import uuid

from backend.models import models
from factory import (LazyFunction, SelfAttribute, Sequence, SubFactory,
                     post_generation)
from factory.alchemy import SQLAlchemyModelFactory

import factories.associations
from factories import BaseMeta, fdt


class DBUser(SQLAlchemyModelFactory):
    """User factory."""
    class Meta(BaseMeta):
        model = models.User
        sqlalchemy_get_or_create = ('sub', 'iss')

    sub = Sequence(lambda n: f"user{n}")
    iss = "egi.com"
    email = Sequence(lambda n: f"user{n}@example.com")


class DBReport(SQLAlchemyModelFactory):
    """Report factory."""
    class Meta(BaseMeta):
        model = models.Report

    id = LazyFunction(uuid.uuid4)
    creation_date = fdt.fuzz()
    verdict = True
    message = Sequence(lambda n: f"Report message {n}")
    uploader = SubFactory(DBUser)


class DBBenchmark(SQLAlchemyModelFactory):
    """Benchmark factory."""
    class Meta(BaseMeta):
        model = models.Benchmark
        sqlalchemy_get_or_create = ('docker_image', 'docker_tag')

    id = LazyFunction(uuid.uuid4)
    docker_image = Sequence(lambda n: f"b{n}")
    docker_tag = "latest"
    description = ""
    json_template = {}
    report_association = SubFactory(factories.associations.DBBenchmarkReport)


class DBSite(SQLAlchemyModelFactory):
    """Site factory."""
    class Meta(BaseMeta):
        model = models.Site
        sqlalchemy_get_or_create = ('name',)

    id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: f"site{n}")
    address = Sequence(lambda n: f"address{n}")
    description = "Text"
    report_association = SubFactory(factories.associations.DBSiteReport)

    @post_generation
    def flavors(self, create, names, **kwargs):
        if names:
            [DBFlavor(site_id=self.id, name=n, **kwargs) for n in names]


class DBFlavor(SQLAlchemyModelFactory):
    """Flavor factory."""
    class Meta(BaseMeta):
        model = models.Flavor
        sqlalchemy_get_or_create = ('name', 'site_id')

    id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: f"flavor{n}")
    description = "Text"
    site_id = LazyFunction(lambda: DBSite().id)
    report_association = SubFactory(factories.associations.DBFlavorReport)


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

    id = LazyFunction(uuid.uuid4)
    json = Sequence(lambda n: {'name': f"report_{n}"})
    uploader = SubFactory(DBUser)
    benchmark = SubFactory(DBBenchmark)
    site = SubFactory(DBSite)
    flavor = SubFactory(DBFlavor, site_id=SelfAttribute('..site.id'))
    report_association = SubFactory(factories.associations.DBResultReport)

    @post_generation
    def tags(self, create, kws, **kwargs):
        if kws:
            self.tags = [DBTag(**kw) for kw in kws]
        else:
            self.tags = []
