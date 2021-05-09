# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from eosc_perf_backend.flavors.models import Flavor
from eosc_perf_backend.sites.models import Site
from eosc_perf_backend.users.models import User
from factory import Sequence, post_generation
from factory.alchemy import SQLAlchemyModelFactory

from . import conftest


class BaseMeta:
    """Factory configuration."""
    # Use the not-so-global scoped_session
    # Warning: DO NOT USE common.Session()!
    sqlalchemy_session = conftest.Session


class FlavorFactory(SQLAlchemyModelFactory):
    """Flavor factory."""
    class Meta(BaseMeta):
        model = Flavor

    name = Sequence(lambda n: f"flavor{n}")
    custom_text = "Text"


class SiteFactory(SQLAlchemyModelFactory):
    """Site factory."""
    class Meta(BaseMeta):
        model = Site

    name = Sequence(lambda n: f"site{n}")
    address = Sequence(lambda n: f"address{n}")
    description = "Text"
    hidden = True

    @post_generation
    def flavors(self, create, flavors, **kwargs):
        flavors = flavors if flavors else [FlavorFactory()]
        [self.flavors.append(x) for x in flavors]


class UserFactory(SQLAlchemyModelFactory):
    """User factory."""
    class Meta(BaseMeta):
        model = User

    sub = Sequence(lambda n: f"user{n}")
    iss = "egi.com"
    email = Sequence(lambda n: f"user{n}@example.com")
