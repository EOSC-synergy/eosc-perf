"""Benchmark models."""
from backend.database import PkModel, db


class Benchmark(PkModel):
    """The benchmark class represents a single type of benchmark that was run.

    Benchmarks are tied down to a specific docker image version to avoid
    confusion and misleading comparisons in case the benchmark images change
    their metrics or scoring scale from version to version.
    """

    docker_image = db.Column(db.Text(), nullable=False)
    docker_tag = db.Column(db.Text(), nullable=False)

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
