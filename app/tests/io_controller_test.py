"""
This module contains unit tests for the IOController class
"""
from time import time
import unittest
import json
from flask import Flask, session
from app.model.database import configure_database
from app.model.facade import DatabaseFacade
from app.controller.authenticator import configure_authenticator
from app.controller.io_controller import controller
from app.configuration import configuration

USER = {'exp': time() + 3600,
        'sub': 'id',
        'info': {'email': 'email@kit.edu',
                 'name': 'John Doe'}}

class IOControllerTest(unittest.TestCase):

    def setUp(self):
        """Called before each test."""
        # set up flask app necessary for flask_sqlalchemy
        self.app = Flask("Test")
        self.app.config['DEBUG'] = True
        self.app.app_context().push()
        self.app.secret_key = '!secret'

        # use memory database, reset entirely every time
        configuration.reload()
        configuration.set('database-path', '')
        configuration.set('debug', True)
        configuration.set('debug-db-reset', True)
        configure_authenticator(self.app)
        configure_database(self.app)

        self.controller = controller
        self.facade = DatabaseFacade()

    def tearDown(self):
        """Called after each test."""
        del self.controller
        del self.facade
        del self.app

    def test_submit_result_unauthenticated(self):
        with self.app.test_request_context():
            self.assertFalse(self.controller.submit_result("", ""))

    def test_submit_result_malformed_json(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(ValueError, self.controller.submit_result, "---", "")

    def test_submit_result_success(self):
        uploader_metadata = '{"id": "' + USER['sub'] + '", "email": "' + USER['info']['email'] + '", "name": "' + USER['info']['name'] + '"}'
        self.facade.add_uploader(uploader_metadata)
        self.facade.add_benchmark("name/name:tag", USER['sub'])
        self.facade.add_site('{"short_name": "name", "address": "100"  }')
        with self.app.test_request_context():
            f = open("app/controller/config/result_template.json")
            template = f.read()
            self._login_standard_user()
            metadata = '{ \
                "uploader": "' + USER["sub"] + '", \
                "benchmark": "name/name:tag", \
                "site": "name" \
            }'
            self.assertTrue(self.controller.submit_result(template, metadata))

    def test_submit_benchmark_unauthenticated(self):
        with self.app.test_request_context():
            self.assertRaises(RuntimeError, self.controller.submit_benchmark, "", "")

    def test_submit_benchmark_malformed_docker_name(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(RuntimeError, self.controller.submit_benchmark, ":", "")
            self.assertRaises(ValueError, self.controller.submit_benchmark, None, "")

    def test_submit_benchmark_success(self):
        uploader_metadata = '{"id": "' + USER['sub'] + '", "email": "' + USER['info']['email'] + '", "name": "' + USER['info']['name'] + '"}'
        self.facade.add_uploader(uploader_metadata)
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertTrue(self.controller.submit_benchmark("mysql", "submit comment."))
            self.assertTrue(self.controller.submit_benchmark("python", ""))

    def test_submit_benchmark_duplicate(self):
        uploader_metadata = '{"id": "' + USER['sub'] + '", "email": "' + USER['info']['email'] + '", "name": "' + USER['info']['name'] + '"}'
        self.facade.add_uploader(uploader_metadata)
        with self.app.test_request_context():
            self._login_standard_user()
            self.controller.submit_benchmark("mysql", "submit comment.")
            self.assertRaises(RuntimeError, self.controller.submit_benchmark, "mysql", "submit comment.")

    def test_submit_site_unauthenticated(self):
        with self.app.test_request_context():
            self.assertFalse(self.controller.submit_site("name", "address"))

    def test_submit_site_invalid_short_name(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(ValueError, self.controller.submit_site, None, "address")
            self.assertRaises(ValueError, self.controller.submit_site, "", "address")

    def test_submit_site_invalid_address(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(ValueError, self.controller.submit_site, "name", None)
            self.assertRaises(ValueError, self.controller.submit_site, "name", "")

    def test_submit_site_success(self):
        uploader_metadata = '{"id": "' + USER['sub'] + '", "email": "' + USER['info']['email'] + '", "name": "' + USER['info']['name'] + '"}'
        self.facade.add_uploader(uploader_metadata)
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertTrue(self.controller.submit_site("name", "127.0.0.1"))

    def test_submit_site_duplicate_name(self):
        uploader_metadata = '{"id": "' + USER['sub'] + '", "email": "' + USER['info']['email'] + '", "name": "' + USER['info']['name'] + '"}'
        self.facade.add_uploader(uploader_metadata)
        with self.app.test_request_context():
            self._login_standard_user()
            self.controller.submit_site("name", "127.0.0.1")
            self.assertFalse(self.controller.submit_site("name", "127.0.0.2"))

    def test_submit_tag_unauthenticated(self):
        with self.app.test_request_context():
            self.assertFalse(self.controller.submit_tag("tag"))

    def test_submit_tag_malformed(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(ValueError, self.controller.submit_tag, None)
            self.assertRaises(ValueError, self.controller.submit_tag, "")

    def test_submit_tag_success(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertTrue(self.controller.submit_tag("tag"))
            self.assertTrue(self.controller.submit_tag("tag2"))

    def test_submit_tag_duplicate(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.controller.submit_tag("tag")
            self.assertFalse(self.controller.submit_tag("tag"))

    def test_get_site_not_found(self):
        with self.app.test_request_context():
            self.assertEqual(self.controller.get_site("name"), None)

    def test_get_site(self):
        uploader_metadata = '{"id": "' + USER['sub'] + '", "email": "' + USER['info']['email'] + '", "name": "' + USER['info']['name'] + '"}'
        self.facade.add_uploader(uploader_metadata)
        with self.app.test_request_context():
            self._login_standard_user()
            self.controller.submit_site("name", "127.0.0.1")
            self.assertEqual(self.controller.get_site("name").get_name(), "name")

    def test_remove_site_not_authenticated(self):
        with self.app.test_request_context():
            self.assertRaises(RuntimeError, self.controller.remove_site, "name")

    def test_remove_site_not_existing(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertFalse(self.controller.remove_site("not existing"))

    def test_remove_site_with_results(self):
        uploader_metadata = '{"id": "' + USER['sub'] + '", "email": "' + USER['info']['email'] + '", "name": "' + USER['info']['name'] + '"}'
        self.facade.add_uploader(uploader_metadata)
        self.facade.add_benchmark("name/name:tag", USER['sub'])
        self.facade.add_site('{"short_name": "name", "address": "100"  }')
        with self.app.test_request_context():
            f = open("app/controller/config/result_template.json")
            template = f.read()
            self._login_standard_user()
            metadata = '{ \
                "uploader": "' + USER["sub"] + '", \
                "benchmark": "name/name:tag", \
                "site": "name" \
            }'
            self.controller.submit_result(template, metadata)
            self.assertRaises(RuntimeError, self.controller.remove_site, "name")

    def test_remove_site(self):
        uploader_metadata = '{"id": "' + USER['sub'] + '", "email": "' + USER['info']['email'] + '", "name": "' + USER['info']['name'] + '"}'
        self.facade.add_uploader(uploader_metadata)
        with self.app.test_request_context():
            self._login_standard_user()
            self.controller.submit_site("name", "127.0.0.1")
            self.assertTrue(self.controller.remove_site("name"))
            # make sure that site is removed
            self.assertFalse(self.controller.remove_site("name"))

    def test_remove_result_not_authenticated(self):
        with self.app.test_request_context():
            self.assertFalse(self.controller.remove_result("name"))

    def test_remove_result_not_admin(self):
        with self.app.test_request_context():        
            self._login_standard_user()
            self.assertFalse(self.controller.remove_result("name"))

    def test_remove_result_not_found(self):
        uploader_metadata = '{"id": "' + USER['sub'] + '", "email": "' + USER['info']['email'] + '", "name": "' + USER['info']['name'] + '"}'
        self.facade.add_uploader(uploader_metadata)
        self.facade.add_benchmark("name/name:tag", USER['sub'])
        self.facade.add_site('{"short_name": "name", "address": "100"  }')
        with self.app.test_request_context():
            f = open("app/controller/config/result_template.json")
            template = f.read()
            self._login_admin()
            metadata = '{ \
                "uploader": "' + USER["sub"] + '", \
                "benchmark": "name/name:tag", \
                "site": "name" \
            }'
            self.controller.submit_result(template, metadata)
            self.assertFalse(self.controller.remove_result("wrong_uuid"))

    def test_remove_result(self):
        uploader_metadata = '{"id": "' + USER['sub'] + '", "email": "' + USER['info']['email'] + '", "name": "' + USER['info']['name'] + '"}'
        self.facade.add_uploader(uploader_metadata)
        self.facade.add_benchmark("name/name:tag", USER['sub'])
        self.facade.add_site('{"short_name": "name", "address": "100"  }')
        with self.app.test_request_context():
            f = open("app/controller/config/result_template.json")
            template = f.read()
            self._login_admin()
            metadata = {
                "uploader": USER["sub"],
                "benchmark": "name/name:tag",
                "site": "name"
            }
            self.controller.submit_result(template, json.dumps(metadata))
            filters = {'filters': [
                {'type': 'uploader', 'value': USER["info"]["email"]},
            ]}
            results = self.facade.query_results(json.dumps(filters))
            self.assertEqual(len(results), 1)
            self.assertTrue(self.controller.remove_result(results[0].get_uuid()))
            # make sure that result is now hidden
            results = self.facade.query_results(json.dumps(filters))
            self.assertEqual(len(results), 0)

    def test_add_current_user_if_missing(self):
        with self.app.test_request_context():
            controller._add_current_user_if_missing()
            self.assertRaises(DatabaseFacade.NotFoundError, self.facade.get_uploader, USER['sub'])
            self._login_standard_user()
            controller._add_current_user_if_missing()
            self.assertTrue(self.facade.get_uploader(USER['sub']))
            controller._add_current_user_if_missing()
            self.assertTrue(self.facade.get_uploader(USER['sub']))

    def test_valid_docker_hub_name(self):
        # TODO: Add tests after method is fixed
        pass

    def test_get_full_name(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertEqual(self.controller.get_full_name(), USER["info"]["name"])
            self._logout()
        with self.app.test_request_context():
            self.assertEqual(self.controller.get_full_name(), None)

    def test_get_email(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertEqual(self.controller.get_email(), USER["info"]["email"])
            self._logout()
        with self.app.test_request_context():
            self.assertEqual(self.controller.get_email(), None)

    def test_get_user_id(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertEqual(self.controller.get_user_id(), USER["sub"])
            self._logout()
        with self.app.test_request_context():
            self.assertEqual(self.controller.get_user_id(), None)

    def test_is_admin_fail_no_affiliations(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertFalse(self.controller.is_admin())
            self._logout()

    def test_is_admin_fail_wrong_affiliations(self):
        with self.app.test_request_context():
            self._login_standard_user()
            session['user']['info']['edu_person_scoped_affiliations'] = ["student@mit.edu"]
            self.assertFalse(self.controller.is_admin())
            self._logout()

    def test_is_admin_one_afilliation(self):
        with self.app.test_request_context():
            self._login_admin()
            self.assertTrue(self.controller.is_admin())
            self._logout()

    def test_is_admin_all_afilliations(self):
        admin_affiliations = configuration.get('debug_admin_affiliations')
        admin_affiliations += ["test@test.edu", "hacker@1337.ccc"]
        # Extending admin affiliations
        configuration.set("debug_admin_affiliations", admin_affiliations)
        with self.app.test_request_context():
            # User has all admin affiliations
            self._login_standard_user()
            session['user']['info']['edu_person_scoped_affiliations'] = admin_affiliations
            self.assertTrue(self.controller.is_admin())
            self._logout()

    def test_authenticated(self):
        """Tests if IOController returns True when logged
           in during is_authenticated method call"""
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertTrue(self.controller.is_authenticated())
            self._logout()

    def test_not_authenticated(self):
        """Tests if IOController returns False when not logged
           in during is_authenticated method call"""
        with self.app.test_request_context():
            self.assertFalse(self.controller.is_authenticated())   

    def _login_standard_user(self):
        session['user'] = USER
        session['user']['info'].pop('edu_person_scoped_affiliations', None)

    def _login_admin(self):
        self._login_standard_user()
        admin_afill = configuration.get('debug_admin_affiliations')[:1]
        session['user']['info']['edu_person_scoped_affiliations'] = admin_afill

    def _logout(self):
        session.pop('user', None)

if __name__ == '__main__':
    unittest.main()
