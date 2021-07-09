"""Tag models."""
from backend.database import PkModel
from sqlalchemy import Column, Text


class Tag(PkModel):
    """The Tag class represents a user-created label that can be used for
    filtering a list of results.

    These are entirely created by users and may not necessarily be related to
    any benchmark output data. These may be used to indicate if, for example, a
    benchmark is used to measure CPU or GPU performance, since some benchmarks
    may be used to test both.
    """

    name = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False, default="")

    def __repr__(self) -> str:
        """Get a human-readable representation string of the tag.

        Returns:
            str: A human-readable representation string of the tag.
        """
        return '<{} {}>'.format(self.__class__.__name__, self.name)
