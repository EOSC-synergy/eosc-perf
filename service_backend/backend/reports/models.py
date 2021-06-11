"""Report models."""
from datetime import datetime

from backend.benchmarks.models import Benchmark
from backend.database import PkModel, db
from backend.results.models import Result
from backend.sites.models import Site, Flavor
from backend.users.models import User


class Report(PkModel):
    """The Report class represents an automated or an user’s report.

    Reports are automated if used to submit new benchmarks or sites, in which
    case the report will need to be approved before the associated site or
    benchmark becomes visible.

    Reports can also be manually generated if users choose to report a result
    from their search results if they suspect it may be falsified or incorrect.
    """
    date = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    verified = db.Column(db.Boolean(), nullable=False, default=False)
    verdict = db.Column(db.Boolean(), nullable=False, default=False)
    message = db.Column(db.Text(), nullable=True)
    uploader = db.relationship("User")

    uploader_iss = db.Column(db.Text(), nullable=False)
    uploader_sub = db.Column(db.Text(), nullable=False)
    __table_args__ = (db.ForeignKeyConstraint(['uploader_iss', 'uploader_sub'],
                                              ['user.iss', 'user.sub']),
                      {})

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'report',
        'polymorphic_on': type
    }

    def __repr__(self) -> str:
        """Get a human-readable representation string of the report.

        Returns:
            str: A human-readable representation string of the report.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.id)


class BenchmarkReport(Report):
    """The BenchmarkReport class represents a report of a benchmark.

    These are automatically generated when a benchmark is submitted.
    """
    id = db.Column(db.UUID, db.ForeignKey('report.id'), primary_key=True)
    benchmark = db.relationship('Benchmark')
    benchmark_id = db.Column(db.ForeignKey('benchmark.id'), nullable=False)
    benchmark_image = db.association_proxy('benchmark', 'docker_image')
    benchmark_tag = db.association_proxy('benchmark', 'docker_tag')

    __mapper_args__ = {
        'polymorphic_identity': 'benchmark_report',
    }

    # TODO: See how to simplify using association_proxy
    @classmethod
    def create(
        cls, uploader_sub, uploader_iss, benchmark_image=None,
        benchmark_tag=None, **kwargs
    ):
        """Extends model create adding most relationship important fields.

        Returns:
            benchmark_report: An instance of Result (stored if commit==True).
        """
        uploader = User.get_by_subiss(
            sub=uploader_sub,
            iss=uploader_iss
        )

        benchmark = Benchmark.filter_by(
            docker_image=benchmark_image,
            docker_tag=benchmark_tag
        ).one()

        return super().create(
            uploader=uploader,
            benchmark=benchmark,
            **kwargs
        )


class ResultReport(Report):
    """The ResultReport class represents a report about a benchmark result.

    These are normally manually generated.
    """
    id = db.Column(db.UUID, db.ForeignKey('report.id'), primary_key=True)
    result = db.relationship('Result')
    result_id = db.Column(db.ForeignKey('result.id'), nullable=False)
    benchmark_image = db.association_proxy('result', 'benchmark_image')
    benchmark_tag = db.association_proxy('result', 'benchmark_tag')
    site_name = db.association_proxy('result', 'site_name')
    flavor_name = db.association_proxy('result', 'flavor_name')

    __mapper_args__ = {
        'polymorphic_identity': 'result_report',
    }

    # TODO: See how to simplify using association_proxy
    @classmethod
    def create(
        cls, uploader_sub, uploader_iss, benchmark_image=None,
        benchmark_tag=None, site_name=None, flavor_name=None, **kwargs
    ):
        """Extends model create adding most relationship important fields.

        Returns:
            result_report: An instance of Result (stored if commit==True).
        """
        uploader = User.get_by_subiss(
            sub=uploader_sub,
            iss=uploader_iss
        )

        result = Result.filter_by(
            benchmark_image=benchmark_image,
            benchmark_tag=benchmark_tag,
            site_name=site_name,
            flavor_name=flavor_name
        ).one()

        return super().create(
            uploader=uploader,
            result=result,
            **kwargs
        )


class SiteReport(Report):
    """The SiteReport class represents a report of a site.

    These are automatically generated when a site is submitted.
    """
    id = db.Column(db.UUID, db.ForeignKey('report.id'), primary_key=True)
    site = db.relationship('Site')
    site_id = db.Column(db.ForeignKey('site.id'), nullable=False)
    site_name = db.association_proxy('site', 'name')

    __mapper_args__ = {
        'polymorphic_identity': 'site_report',
    }

    # TODO: See how to simplify using association_proxy
    @classmethod
    def create(
        cls, uploader_sub, uploader_iss, site_name=None, **kwargs
    ):
        """Extends model create adding most relationship important fields.

        Returns:
            site_report: An instance of Result (stored if commit==True).
        """
        uploader = User.get_by_subiss(
            sub=uploader_sub,
            iss=uploader_iss
        )

        site = Site.filter_by(
            name=site_name
        ).one()

        return super().create(
            uploader=uploader,
            site=site,
            **kwargs
        )


class FlavorReport(Report):
    """The FlavorReport class represents a report of a flavor.

    These are automatically generated when a flavor is submitted.
    """
    id = db.Column(db.UUID, db.ForeignKey('report.id'), primary_key=True)
    site = db.relationship('Site')
    site_id = db.Column(db.ForeignKey('site.id'), nullable=False)
    flavor = db.relationship('Flavor')
    flavor_id = db.Column(db.ForeignKey('flavor.id'), nullable=False)
    site_name = db.association_proxy('site', 'name')
    flavor_name = db.association_proxy('flavor', 'name')

    __mapper_args__ = {
        'polymorphic_identity': 'flavor_report',
    }

    # TODO: See how to simplify using association_proxy
    @classmethod
    def create(
        cls, uploader_sub, uploader_iss, site_name=None, flavor_name=None, **kwargs
    ):
        """Extends model create adding most relationship important fields.

        Returns:
            flavor_report: An instance of Result (stored if commit==True).
        """
        uploader = User.get_by_subiss(
            sub=uploader_sub,
            iss=uploader_iss
        )

        site = Site.filter_by(
            name=site_name
        ).join(Site.flavors).filter_by(
            name=flavor_name
        ).one()

        flavor = Flavor.filter_by(
            site_id=site.id,
            name=flavor_name
        ).one()

        return super().create(
            uploader=uploader,
            site=site,
            flavor=flavor,
            **kwargs
        )
