# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from attr import __description__
from factory import post_generation, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from eosc_perf.database import db
from eosc_perf.flavors.models import Flavor
from eosc_perf.sites.models import Site
from eosc_perf.users.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""
    class Meta:
        """Factory configuration."""
        abstract = True
        sqlalchemy_session = db.session


class FlavorFactory(BaseFactory):
    """Flavor factory."""
    class Meta:
        model = Flavor

    name = Sequence(lambda n: f"flavor{n}")
    custom_text = Sequence(lambda n: f"Text {n}")


class SiteFactory(BaseFactory):
    """Site factory."""
    class Meta:
        model = Site

    name = Sequence(lambda n: f"site{n}")
    address = Sequence(lambda n: f"address{n}")
    description = Sequence(lambda n: f"Desc {n}")
    hidden = True

    @post_generation
    def flavors(obj, create, extracted, **kwargs):
        return extracted or [UserFactory(name=x) for x in obj.flavors]


class UserFactory(BaseFactory):
    """User factory."""
    class Meta:
        model = User

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.com")
    active = True
