# -*- coding: utf-8 -*-
"""User models."""
from eosc_perf_backend.database import PkModel, db


class Benchmark(PkModel):
    """The benchmark class represents a single type of benchmark that was run.

    Benchmarks are tied down to a specific docker image version to avoid confusion and misleading comparisons in case
    the benchmark images change their metrics or scoring scale from version to version.
    """

    docker_name = db.Column(db.Text(), unique=True, nullable=False)
    template = db.Column(db.Text, nullable=True)
    hidden = db.Column(db.Boolean, default=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    uploader = db.relationship("User")
    uploader_iss = db.Column(db.Text(), nullable=False)
    uploader_sub = db.Column(db.Text(), nullable=False)
    __table_args__ = (
        db.ForeignKeyConstraint(
            ["uploader_iss", "uploader_sub"], ["user.iss", "user.sub"]
        ),
    )

    def __repr__(self) -> str:
        """Get a human-readable representation string of the benchmark.

        Returns:
            str: A human-readable representation string of the benchmark.
        """
        return "<{} {}>".format(self.__class__.__name__, self.docker_name)
