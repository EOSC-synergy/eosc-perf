# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from eosc_perf.database import db
from eosc_perf.flavors.models import Flavor
from eosc_perf.users.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""
        abstract = True
        sqlalchemy_session = db.session


class FlavorFactory(BaseFactory):
    """Flavor factory."""
    name = Sequence(lambda n: f"flavor{n}")
    custom_text = Sequence(lambda n: f"Text {n}")

    class Meta:
        model = Flavor


class UserFactory(BaseFactory):
    """User factory."""
    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.com")
    active = True

    class Meta:
        model = User
