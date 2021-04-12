# -*- coding: utf-8 -*-
"""User models."""
from eosc_perf.database import PkModel, db
from eosc_perf.users.models import Uploader


class Benchmark(PkModel):
    """The benchmark class represents a single type of benchmark that was run.

    Benchmarks are tied down to a specific docker image version to avoid confusion and misleading comparisons in case
    the benchmark images change their metrics or scoring scale from version to version.
    """
    docker_name = db.Column(db.Text(), nullable=False, primary_key=True)
    hidden = db.Column(db.Boolean, nullable=False, default=True)
    uploader_id = db.Column(db.ForeignKey(Uploader.id))
    uploader = db.relationship(Uploader)
    description = db.Column(db.Text, nullable=True)
    template = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        """Get a human-readable representation string of the benchmark.

        Returns:
            str: A human-readable representation string of the benchmark.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.docker_name)
