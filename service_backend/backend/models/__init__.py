"""Backend package for models definition. Includes all necessary models
to store benchmark results with all the necessary contextual information.
"""
from .models.benchmark import Benchmark
from .models.flavor import Flavor
from .models.report import Report
from .models.result import Result
from .models.site import Site
from .models.tag import Tag
from .models.user import User

__all__ = [
    "Benchmark",
    "Report",
    "Result",
    "Site",
    "Flavor",
    "Tag",
    "User"
]
