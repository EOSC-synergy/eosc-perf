"""Result models."""
from backend.benchmarks.models import Benchmark
from backend.database import PkModel, db
from backend.sites.models import Flavor, Site
from backend.tags.models import Tag
from backend.users.models import User
from sqlalchemy import or_

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

    json = db.Column(db.Jsonb, nullable=False)
    tags = db.relationship(Tag, secondary=tag_association)
    tag_names = db.association_proxy('tags', 'name')

    benchmark_id = db.Column(db.ForeignKey('benchmark.id'), nullable=False)
    benchmark = db.relationship(Benchmark)
    docker_image = db.association_proxy('benchmark', 'docker_image')
    docker_tag = db.association_proxy('benchmark', 'docker_tag')

    site_id = db.Column(db.ForeignKey('site.id'), nullable=False)
    site = db.relationship(Site)
    site_name = db.association_proxy('site', 'name')

    flavor_id = db.Column(db.ForeignKey('flavor.id'), nullable=False)
    flavor = db.relationship(Flavor)
    flavor_name = db.association_proxy('flavor', 'name')

    uploader_iss = db.Column(db.Text, nullable=False)
    uploader_sub = db.Column(db.Text, nullable=False)
    uploader = db.relationship(User)
    __table_args__ = (db.ForeignKeyConstraint(['uploader_iss', 'uploader_sub'],
                                              ['user.iss', 'user.sub']),
                      {})

    def __repr__(self) -> str:
        """Get a human-readable representation string of the result.

        Returns:
            str: A human-readable representation string of the result.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.id)

    @classmethod
    def query_with(cls, terms):
        """Query all results containing all keywords in the columns.

        Args:
            terms (List[str]): A list of all keywords that need to be matched.
        Returns:
            List[Result]: A list containing all matching query results in the
            database.
        """
        results = cls.query
        for keyword in terms:
            results = results.filter(
                or_(
                    # TODO: Result.json.contains(keyword),
                    Result.docker_image.contains(keyword),
                    Result.docker_tag.contains(keyword),
                    Result.site_name.contains(keyword),
                    Result.flavor_name.contains(keyword),
                    Result.tag_names == keyword
                ))

        return results
