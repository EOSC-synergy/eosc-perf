"""Result models."""
from backend.benchmarks.models import Benchmark
from backend.database import PkModel, db
from backend.sites.models import Flavor, Site
from backend.tags.models import Tag
from backend.users.models import User

tag_association = db.Table(
    'result_tags',
    db.Column('result_id', db.UUID, db.ForeignKey('result.id')),
    db.Column('tag_id', db.UUID, db.ForeignKey('tag.id')),
    db.PrimaryKeyConstraint('result_id', 'tag_id')
)


class Result(PkModel):
    """The Result class represents a single benchmark result and its contents.

    They carry the JSON data output by the ran benchmarks.
    """

    json = db.Column(db.Json, nullable=False)
    tags = db.relationship("Tag", secondary=tag_association)
    tag_names = db.association_proxy('tags', 'name')

    benchmark = db.relationship("Benchmark")
    benchmark_id = db.Column(
        db.UUID(binary=False),
        db.ForeignKey('benchmark.id'),
        nullable=False
    )
    benchmark_image = db.association_proxy('benchmark', 'docker_image')
    benchmark_tag = db.association_proxy('benchmark', 'docker_tag')

    site = db.relationship("Site")
    site_id = db.Column(
        db.UUID(binary=False),
        db.ForeignKey('site.id'),
        nullable=False
    )
    site_name = db.association_proxy('site', 'name')

    flavor = db.relationship("Flavor")
    flavor_id = db.Column(
        db.UUID(binary=False),
        db.ForeignKey('flavor.id'),
        nullable=False
    )
    flavor_name = db.association_proxy('flavor', 'name')

    uploader = db.relationship("User")
    uploader_iss = db.Column(db.Text, nullable=False)
    uploader_sub = db.Column(db.Text, nullable=False)
    __table_args__ = (db.ForeignKeyConstraint(['uploader_iss', 'uploader_sub'],
                                              ['user.iss', 'user.sub']),
                      {})

    def __repr__(self) -> str:
        """Get a human-readable representation string of the result.

        Returns:
            str: A human-readable representation string of the result.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.id)

    # TODO: See how to simplify using association_proxy
    @classmethod
    def create(
        cls, benchmark_image, benchmark_tag, site_name, flavor_name, uploader_sub,
        uploader_iss, tag_names=[], **kwargs
    ):
        """Extends model create adding most relationship important fields.

        Returns:
            result: An instance of Result (stored if commit==True).
        """
        _uploader = User.get_by_subiss(
            sub=uploader_sub,
            iss=uploader_iss
        )

        _benchmark = Benchmark.filter_by(
            docker_image=benchmark_image,
            docker_tag=benchmark_tag
        ).one()

        _site = Site.filter_by(
            name=site_name
        ).one()

        _flavor = Flavor.filter_by(
            site_id=_site.id,
            name=flavor_name
        ).one()

        _tags = Tag.query.filter(
            Tag.name.in_(tag_names)
        ).all()
        if len(tag_names) != len(_tags):
            raise db.exc.NoResultFound

        return super().create(
            uploader=_uploader, benchmark=_benchmark, site=_site,
            flavor=_flavor, tags=_tags, **kwargs
        )

    # TODO: See how to simplify using association_proxy
    def update(
        self, benchmark_image=None, benchmark_tag=None, site_name=None,
        flavor_name=None, uploader_sub=None, uploader_iss=None, tag_names=None,
        **kwargs
    ):
        """Extends model create adding most relationship important fields.

        Returns:
            result: An instance of Result (stored if commit==True).
        """
        if benchmark_image:
            if benchmark_tag:
                new_benchmark = Benchmark.query.filter_by(
                    docker_image=benchmark_image,
                    docker_tag=benchmark_tag
                ).one()
            else:
                new_benchmark = Benchmark.query.filter_by(
                    docker_image=benchmark_image,
                    docker_tag=self.benchmark.docker_tag
                ).one()
            self.benchmark = new_benchmark

        elif benchmark_tag:
            new_benchmark = Benchmark.query.filter_by(
                docker_image=self.benchmark.docker_image,
                docker_tag=benchmark_tag
            ).one()
            self.benchmark = new_benchmark

        if site_name:
            new_site = Site.query.filter_by(
                name=site_name
            ).one()
            self.site = new_site

            if flavor_name:
                new_flavor = Flavor.query.filter_by(
                    site_id=new_site.id,
                    name=flavor_name
                ).one()
            else:
                new_flavor = Flavor.query.filter_by(
                    site_id=new_site.id,
                    name=self.flavor.name
                ).one()
            self.flavor = new_flavor

        else:
            if flavor_name:
                new_flavor = Flavor.query.filter_by(
                    site_id=self.site.id,
                    name=flavor_name
                ).one()
                self.flavor = new_flavor

        # TODO: User update

        if tag_names:
            new_tags = Tag.query.filter(Tag.name.in_(tag_names)).all()
            if len(tag_names) != len(new_tags):
                raise db.exc.NoResultFound
            else:
                self.tags = new_tags

        return super().update(**kwargs)
