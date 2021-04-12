# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for

from eosc_perf.user.models import User

from .factories import UserFactory


class TestLoggingIn:
    """Login."""

    def test_can_log_in_returns_200(self, user, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms["loginForm"]
        form["username"] = user.username
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms["loginForm"]
        form["username"] = user.username
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for("auth.logout")).follow()
        # sees alert
        assert "You are logged out." in res


class TestRegistering:
    """Register a user."""

    def test_can_register(self, user, testapp):
        """Register a new user."""
        old_count = len(User.query.all())
        # Goes to homepage
        res = testapp.get("/")
        # Clicks Create Account button
        res = res.click("Create account")
        # Fills out the form
        form = res.forms["registerForm"]
        form["username"] = "foobar"
        form["email"] = "foo@bar.com"
        form["confirm"] = "secret"
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_sees_error_message_if_user_already_registered(self, user, testapp):
        """Show error if user already registered."""
        user = UserFactory(active=True)  # A registered user
        user.save()
        # Goes to registration page
        res = testapp.get(url_for("public.register"))
        # Fills out form, but username is already registered
        form = res.forms["registerForm"]
        form["username"] = user.username
        form["email"] = "foo@bar.com"
        form["confirm"] = "secret"
        # Submits
        res = form.submit()
        # sees error
        assert "Username already registered" in res
