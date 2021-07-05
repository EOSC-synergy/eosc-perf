"""Benchmark models."""
from backend.database import PkModel, db
from sqlalchemy import or_


class Benchmark(PkModel):
    """The benchmark class represents a single type of benchmark that was run.

    Benchmarks are tied down to a specific docker image version to avoid
    confusion and misleading comparisons in case the benchmark images change
    their metrics or scoring scale from version to version.
    """

    docker_image = db.Column(db.Text(), nullable=False)
    docker_tag = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), default="")
    json_template = db.Column(db.Json, default={})

    __table_args__ = (
        db.UniqueConstraint('docker_image', 'docker_tag'),
    )

    def __repr__(self) -> str:
        """Get a human-readable representation string of the benchmark.

        Returns:
            str: A human-readable representation string of the benchmark.
        """
        return "<{} {}:{}>".format(
            self.__class__.__name__,
            self.docker_image,
            self.docker_tag
        )

    @classmethod
    def query_with(cls, terms):
        """Query all benchmarks containing all keywords in the name.

        Args:
            terms (List[str]): A list of all keywords that need to be in the
            benchmark's docker name.
        Returns:
            List[Benchmark]: A list containing all matching benchmarks in the
            database.
        """
        results = cls.query
        for keyword in terms:
            results = results.filter(
                or_(
                    Benchmark.docker_image.contains(keyword),
                    Benchmark.docker_tag.contains(keyword),
                    Benchmark.description.contains(keyword)
                ))

        return results
