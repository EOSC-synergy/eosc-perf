# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from attr import __description__
from eosc_perf.database import db
from eosc_perf.flavors.models import Flavor
from eosc_perf.sites.models import Site
from eosc_perf.users.models import User
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
    custom_text = Sequence(lambda n: f"Text {n}")


class SiteFactory(SQLAlchemyModelFactory):
    """Site factory."""
    class Meta(BaseMeta):
        model = Site

    name = Sequence(lambda n: f"site{n}")
    address = Sequence(lambda n: f"address{n}")
    description = Sequence(lambda n: f"Desc {n}")
    hidden = True
    flavors = []


class UserFactory(SQLAlchemyModelFactory):
    """User factory."""
    class Meta(BaseMeta):
        model = User

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.com")
    active = True
