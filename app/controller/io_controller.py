"""
This module acts as a facade between view and model.
"""
import json
from re import match
from typing import List
from requests import get
from requests_html import HTMLSession
from .json_result_validator import JSONResultValidator
from .authenticator import Authenticator
from .type_aliases import USER, JSON, AuthenticateError
from ..model.facade import DatabaseFacade, facade
from ..model.data_types import Benchmark, Site, Report
# The parent url of docker hub projects, first for private second for docker certified.
docker_hub_url = {"certified": "https://hub.docker.com/r/",
                  "default": "https://hub.docker.com/_/"}
# For debugging skips the authentication process
DEBUG = True


class IOController:
    """This class acts as a facade between view and model, and validate user input.
    Attributes:
    __result_validator  (JSONResultValidator): The validator for an uploaded benchmark result.
    __database_facade        (DatabaseFacade): The facade to interact with the model.
    __unapproved_benchmarks (List[Benchmark]): The user suggested unaproved benchmarks.
    __unapproved_sites           (List[Site]): The user suggested unaproved sites."""

    def __init__(self, database_facade: DatabaseFacade = None, unapproved_sites: List[Site] = [],
                 unapproved_benchmarks: List[Benchmark] = []):
        """Constructor generat a new instance of IOController.
        Args:
        data_base (DatabaseFacade): The facade used to interact with the model if left
                                    empty creates a new facade and there for a new database.
        unapproved_sites (List[Site]): A list of unaproved Sites can be left empty.
        unapproved_benchmarks (List[Benchmark]): A list of unaproved Benchmarks can be left empty.
        """
        # TODO: Find better solution for database_facade since it is supposed to be Singelton.
        self.__result_validator = JSONResultValidator()
        self.__unapproved_sites = unapproved_sites
        self.__unapproved_benchmarks = unapproved_benchmarks
        if database_facade is None:
            self.__database_facade = DatabaseFacade()
        else:
            self.__database_facade = DatabaseFacade

    def authenticate(self, current_user: USER) -> bool:
        """Authenticate the current user.
        Args:
        current_user (USER): The current user to get authenticated.
        Returns:
        bool: True if the user is authenticated."""
        # TODO remove.
        if DEBUG:
            return True
        # Using lazyevaluation of python.
        return Authenticator.is_authenticated(current_user) or \
            Authenticator.authenticate_user(current_user)

    def submit_result(self, result_json: str, metadata: str, current_user: USER) -> bool:
        """Submit a new benchmark result to the system if it is valid.
            Fails if the user isn't authenticated or the result json is in an invalid format.
        Args:
        result_json  (JSON): The benchmark result.
        metadata      (str): The metadata associated with the benchmark result.
        current_user (USER): The user submitting the new result.
        Returns:
        bool: If the benchmark was successfully added.
        """
        # Check if user is authenticated
        if self.authenticate(current_user):
            # Check if the result is in the correct format.
            if self.__result_validator  .validate_json(result_json):
                # Try to add the result to the data base.
                return self.__database_facade.add_result(result_json, metadata)
        return False

    def submit_benchmark(self, uploader_email: str, current_user: USER, docker_name: str,
                         check_for_page: bool = False) -> bool:
        """Submit a new Benchmark to the system.
        Args:
        uploader_email  (str): The email address of the uploader.
        docker_name     (str): The name of the dockerhub reposetory and sub url.
                               So that https://hub.docker.com/_/[docker_name] or
                               https://hub.docker.com/_/[docker_name] results in a valid url.
        current_user   (USER): The user who submits the Benchmark.
        check_for_page (bool): Determines whether to control if the url corresponds to
                               an existing image on docker hub. Can lead to problems if
                               chromium isn't installed
                               and takes a considerable amount of time (5-10s).
        Returns:
        bool: If the benchmark was successfully submitted.
        """
        # Check if user is authenticated.
        if not self.authenticate(current_user):
            return False
        # Check for valid email address.
        if match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\Z)", uploader_email) is None:
            return False
        # Check valid docker_hub_name.
        if self.__valid_docker_hub_name(docker_name, check_for_page):
            # Add to model.
            return facade.add_benchmark(
                docker_name=docker_name, uploader_email=uploader_email)
        return False

    def get_unapproved_benchmarks(self, current_user: USER) -> List[Benchmark]:
        """If the current user is an admin, get a list of all unapproved benchmarks.
        Args:
        current_user (USER): The user trying to get the unaproved Benchmarks.
        Returns:
        List[Benchmark]: List of unaproved Benchmarks.
        """
        if Authenticator.is_admin(current_user):
            return self.__unapproved_benchmarks
        raise AuthenticateError('The user isn\'t an admin.')

    def approve_benchmark(self, current_user: USER, benchmark: Benchmark = None,
                          benchmark_name: str = None) -> bool:
        """Approve a Benchmark, requires the current user to be an admin.
        Args:
        current_user   (USER): The user trying to approve a benchmark.
        benchmark (Benchmark): The benchmark to be approved.
        benchmark_name  (str): The name of the previously unapproved benchamark to get approved.
                               Is only used if benchmark is left empty.
        Returns:
        bool: If the benchmark was successfully approved.
        """
        # Select the right benchmark.
        if benchmark is None:
            for single_benchmark in self.__unapproved_benchmarks:
                if single_benchmark.get_docker_name() is benchmark_name:
                    benchmark = single_benchmark
                    break
        # Ensure there is a benchmark to add.
        if benchmark is None:
            return False
        # Add the benchmark to the model.
        if Authenticator.is_admin(current_user):
            if facade.add_benchmark(benchmark.get_docker_name(), benchmark.get_uploader()):
                # Was successfully added.
                for single_benchmark in self.__unapproved_benchmarks:
                    # Remove from __unaproved_benchmarks.
                    if single_benchmark.get_docker_name() is benchmark.get_docker_name():
                        self.__unapproved_benchmarks.remove(single_benchmark)
                        break
                return True
        return False

    def submit_site(self, metadata_json: JSON, current_user: USER) -> bool:
        """Submit a new site, will be aviable after getting approved.
        Args:
        metadata_json (JSON): A json formated str containing a 'short_name' and 'address' parameter
                              ,as well as maybe a 'name' parameter.
        current_user  (USER): The user submitting the side.
        Returns:
        bool: If the submission was successful.
        """
        if self.authenticate(current_user):
            # Crete new site.
            new_site = self.__parse_site(metadata_json)
            # Add to unaproved sites.
            if not new_site is None:
                self.__unapproved_sites.append(new_site)
                return True
        return False

    def get_unapproved_sites(self, current_user: USER) -> List[Site]:
        """If the current user is an admin provide a list of all unaproved sites.
        Args:
        current_user (USER): The user requesting the unapproved sites.
        Returns:
        List[Sites]: All unaproved sites, can be empty.
        """
        # Check if admin.
        if Authenticator.is_admin(current_user):
            return self.__unapproved_sites
        # User isn't admin.
        raise AuthenticateError(
            "The users attempting to get teh unapproved sites isn't an an admin.")

    def approve_site(self, current_user: USER, site: Site = None, metadata_json: JSON = None) \
            -> bool:
        """If the current user is an admin, approve the given site.
        Args:
        current_user  (USER): The user attempting to approve the site.
        site          (Site): The admin reviewed site getting add to the model.
        metadata_json (JSON): A json formated str containing a 'short_name' and 'address' parameter
                              ,as well as maybe a 'name' parameter. Gets used if site is left empty.
        Returns:
        bool: If process was successful.
        """

        # Check if user is allowed to approve.
        if Authenticator.is_admin(current_user):
            # Decide whether to use site or metadata_json.
            site = [site, self.__parse_site(metadata_json)][site is None]
            if not site is None:
                # Atm unnecessary step, but usefull in case the site got created not in
                # IOController or DatabaseFacade.
                json_str = '{ '+'"short_name" : "' + site.get_short_name() + \
                           '" , "address" : "' + site.get_address() + \
                           '" , "name" : "' + site.get_name() + \
                           '" , "description" : "' + site.get_description() + '" ' + '}'
                # Try to add to database.
                if self.__database_facade.add_site(json_str):
                    # Successfully added, remove from __unapproved_sites.
                    for singel_site in self.__unapproved_sites:
                        # one of the attributes enough in case a admin corrected eg. the addres.
                        if singel_site.get_short_name() is site.get_short_name() or \
                                singel_site.get_address() is site.get_address():
                            self.__unapproved_sites.remove(singel_site)
                            break
                    return True
        return False

    def report(self, current_user: USER, metadata: JSON) -> bool:
        """Add a Report to the model, and notify an admin about it.
        Args:
        current_user (USER): The user reporting a result.
        metadata     (JSON): The metadata in json format, containing the
                             benchmark 'result_id' and the associated 'user_message'.
        Returns:
        bool: If the report was successfully added.
        """
        if self.authenticate(current_user):
            # Add to database.
            if self.__database_facade.add_report(metadata):
                # TODO: notify admin, per email.
                return True
        return False

    def get_report(self, current_user: USER, only_unanswered: bool = False) -> List[Report]:
        """Provide a list of all reports, require the user to be an admin.
        Args:
        current_user    (USER): The user accessing the reports.
        only_unanswered (bool): Whether all or only the unanswered, reports get provided.
        Returns:
        List[Reports]: List of all the requested reports, throws an AuthenticationError if
                       the authentication failed."""
        if Authenticator.is_admin(current_user):
            return self.__database_facade.get_reports(only_unanswered=only_unanswered)
        raise AuthenticateError(
            "User trying to view the reports isn't an admin.")

    def process_report(self, verdict: bool, current_user: USER, uuid: str = None,
                       report: Report = None) -> bool:
        """Add the verdict to the model, if the verdict consents the report the associated
        benchmark gets deleted.
        Args:
        verdict      (bool): The verdict True when agreeing with the report False otherwise.
        current_user (USER): The user jugging the report.
        uuid          (str): The uuid of the jugged report, gets used if report is left empty.
        report     (Report): The report jugged.
        Returns:
        bool: If the process was successful.
        """
        # Check if user is admin.
        if Authenticator.is_admin(current_user):
            # Search report from model, incase the input report somehow got copied.
            # Select uuid if report is left empty.
            uuid = [report.get_uuid, uuid][report is None]
            # Ensure one of both isn't None.
            if uuid is None:
                return False
            # Set the verdict.
            try:
                report_by_uuid = self.__database_facade.get_report(uuid)
                # Set the verdict status.
                report_by_uuid.set_verdict(verdict)
                # Delete Benchmark if necessary
                if verdict:
                    # TODO: Delete Benchmark or mark somehow as invalid.
                    pass
            except AttributeError:
                # There is no report with given uuid.
                return False
            return True
        return False

    def __valid_docker_hub_name(self, docker_name: str, check_for_page: bool) -> bool:
        """Check if it is a valid docker hub name.
        Therefore controll the naming convention and if the corrensponding docker hub page,
        is existing.
        Args:
        docker_name      (str): The url to the docker hub page.
        check_for_page  (bool): Determines whether to control if the url corresponds to
                                an existing image on docker hub.
        Returns:
        bool: If it is a valid docker name.
        """
        # Distinguish between docker certified, and not docker certified.
        if "/" in docker_name:
            user_name, image_name = docker_name.split("/", 1)
            url_prefix = docker_hub_url['default']
            # controll valid docker id (https://docs.docker.com/docker-id/).
            if match(r'^([a-z]|[0,9]){4,30}\Z', user_name) is None:
                return False
        else:
            image_name = docker_name
            url_prefix = docker_hub_url['certified']
        url = url_prefix+docker_name
        # Controll the naming conventions (https://docs.docker.com/docker-hub/repos/).
        if not match(r'^([a-z]|[0,9]|[-,_]){2,255}\Z', image_name) is None:
            if not check_for_page:
                return True
            # Check if the page exists.
            try:
                get(url)
            except ConnectionError:
                return False
            # Load the http.
            else:
                session = HTMLSession()
                content = session.get(url)
                # Might install chromium.
                # Timeconsuming Step
                content.html.render()
                rendered_contend = content.html.search('<body{}/body>')
                # Exclude the default empty page on dockerhub.
                return not any(map(lambda x: 'data-testid="404page" alt="404 Route Not Found"'
                                   in x, rendered_contend))
        return False

    def __parse_site(self, metadata_json: JSON) -> Site:
        """Create a new site using a metadata json formated object.
        Args:
        metadata_json (JSON): A json formated str containing a 'short_name' and 'address' parameter
                              ,as well as maybe a 'name' parameter.
        Returns:
        Site: The new created Site object, is None if metadata_json doesn't
              contain the required parameters.
        """
        metadata = None
        try:
            metadata = json.loads(metadata_json)
        except json.JSONDecodeError:
            return None
        site = None
        # Helper function controlls that parameter is in metadata
        # and the associated value isn't empty.
        contained = lambda a: a in metadata and bool(a)
        # input validation
        if all(map(contained, ['short_name', 'address'])):
            # Create with or without name.
            if contained('name'):
                site = Site(metadata['short_name'],
                            metadata['address'], name=metadata['name'])
            else:
                site = Site(metadata['short_name'], metadata['address'])
            # add description if contaiend in metadata.
            if contained('description'):
                site.set_description(metadata['description'])
        return site
