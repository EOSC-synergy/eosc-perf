from typing import List
import code
from app import create_app
from app.model.database import db
from app.model.sandbox import add_dummies_if_not_exist, results, benchmarks, sites, tags, uploaders
from app.model.data_types import Uploader, Tag, Result, Benchmark, Site, ResultIterator, Report, \
    SiteReport, BenchmarkReport, ResultReport
from app.model.facade import facade

# utility helpers for functions not part of design


def get_uploaders() -> List[Uploader]:
    """Get all uploaders."""
    # prepare query
    return db.session.query(Uploader).all()


def get_benchmarks() -> List[Benchmark]:
    """Get all benchmarks."""
    # prepare query
    return db.session.query(Benchmark).all()


app = create_app(True)

add_dummies_if_not_exist(app)

code.interact(local=locals())
