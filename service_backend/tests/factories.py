"""Factories to help in tests."""
import uuid
from datetime import datetime

from backend.benchmarks.models import Benchmark
from backend.reports.models import BenchmarkReport, ResultReport, SiteReport
from backend.results.models import Result
from backend.sites.models import Flavor, Site
from backend.tags.models import Tag
from backend.users.models import User
from factory import (LazyFunction, SelfAttribute, Sequence,
                     SubFactory, post_generation)
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyNaiveDateTime

from . import conftest

fdt = FuzzyNaiveDateTime(datetime(2000, 1, 1))


class BaseMeta:
    """Factory configuration."""
    # Use the not-so-global scoped_session
    # Warning: DO NOT USE common.Session()!
    sqlalchemy_session = conftest.Session


class BenchmarkFactory(SQLAlchemyModelFactory):
    """Benchmark factory."""
    class Meta(BaseMeta):
        model = Benchmark
        sqlalchemy_get_or_create = ('docker_image', 'docker_tag')

    id = LazyFunction(uuid.uuid4)
    docker_image = Sequence(lambda n: f"b{n}")
    docker_tag = "latest"


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


class SiteFactory(SQLAlchemyModelFactory):
    """Site factory."""
    class Meta(BaseMeta):
        model = Site
        sqlalchemy_get_or_create = ('name',)

    id = LazyFunction(uuid.uuid4)
    name = Sequence(lambda n: f"site{n}")
    address = Sequence(lambda n: f"address{n}")
    description = "Text"

    @post_generation
    def flavors(self, create, names, **kwargs):
        if names:
            [FlavorFactory(site_id=self.id, name=n, **kwargs) for n in names]


class FlavorFactory(SQLAlchemyModelFactory):
    """Flavor factory."""
    class Meta(BaseMeta):
        model = Flavor
        sqlalchemy_get_or_create = ('name', 'site_id')

    name = Sequence(lambda n: f"flavor{n}")
    description = "Text"
    site_id = None


class ResultFactory(SQLAlchemyModelFactory):
    """Result factory."""
    class Meta(BaseMeta):
        model = Result

    json = Sequence(lambda n: {'name': f"report_{n}"})
    benchmark = SubFactory(BenchmarkFactory)
    site = SubFactory(SiteFactory)
    flavor = SubFactory(FlavorFactory, site_id=SelfAttribute('..site.id'))
    uploader = SubFactory(UserFactory)

    @post_generation
    def tags(self, create, kws, **kwargs):
        if kws:
            self.tags = [TagFactory(**kw) for kw in kws]
        else:
            self.tags = []






class BenchmarkReportFactory(SQLAlchemyModelFactory):
    """BenchmarkReport factory."""
    class Meta(BaseMeta):
        model = BenchmarkReport

    docker_image = Sequence(lambda n: f"benchmark{n}")
    date = fdt.fuzz()
    verified = True
    verdict = True
    message = "Benchmark report message"
    uploader = SubFactory(UserFactory)
