"""Factories module to define the main model factories"""
import uuid

from backend import models
from factory import LazyFunction, Sequence, SubFactory, post_generation
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


class DBBenchmark(SQLAlchemyModelFactory):
    """Benchmark factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.Benchmark
        sqlalchemy_get_or_create = ('id',)

    id = LazyFunction(uuid.uuid4)
    upload_datetime = fdt.fuzz()
    docker_image = Sequence(lambda n: f"benchmark {n}")
    docker_tag = "latest"
    description = "Benchmark example"
    json_schema = {"properties": {"time": {"type": "integer"}}}
    upload_datetime = fdt.fuzz()
    uploader = SubFactory(DBUser)

    @post_generation
    def status(self, create, status, **kwargs):
        if not status or status == "on_review":
            pass
        elif status == "approved":
            self.approve()
        else:
            raise RuntimeError(f"bad status {status}")


class DBSite(SQLAlchemyModelFactory):
    """Site factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.Site
        sqlalchemy_get_or_create = ('id',)

    id = LazyFunction(uuid.uuid4)
    upload_datetime = fdt.fuzz()
    name = Sequence(lambda n: f"site{n}")
    address = Sequence(lambda n: f"address{n}")
    description = "Text"
    upload_datetime = fdt.fuzz()
    uploader = SubFactory(DBUser)

    @post_generation
    def status(self, create, status, **kwargs):
        if not status or status == "on_review":
            pass
        elif status == "approved":
            self.approve()
        else:
            raise RuntimeError(f"bad status {status}")


class DBFlavor(SQLAlchemyModelFactory):
    """Flavor factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.Flavor
        sqlalchemy_get_or_create = ('id',)

    id = LazyFunction(uuid.uuid4)
    upload_datetime = fdt.fuzz()
    name = Sequence(lambda n: f"flavor{n}")
    description = "Text"
    site = SubFactory(DBSite)
    upload_datetime = fdt.fuzz()
    uploader = SubFactory(DBUser)

    @post_generation
    def status(self, create, status, **kwargs):
        if not status or status == "on_review":
            pass
        elif status == "approved":
            self.approve()
        else:
            raise RuntimeError(f"bad status {status}")


class DBTag(SQLAlchemyModelFactory):
    """Tag factory. Default kwargs are:"""
    class Meta(BaseMeta):
        model = models.Tag
        sqlalchemy_get_or_create = ('id',)

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
    json = Sequence(lambda n: {'name': f"result_{n}"})
    benchmark = SubFactory(DBBenchmark)
    flavor = SubFactory(DBFlavor)
    upload_datetime = fdt.fuzz()
    uploader = SubFactory(DBUser)

    @post_generation
    def tags(self, create, specs, **kwargs):
        specs = specs if specs is not None else []
        for spec in specs:
            tag = DBTag(**{**spec, **kwargs})
            self.tags.append(tag)

    @post_generation
    def claims(self, create, messages, **kwargs):
        if messages:
            for msg in messages:
                self._claim_report_class(
                    uploader=DBUser(),
                    message=msg,
                    resource=self
                ).approve()
            self.delete
