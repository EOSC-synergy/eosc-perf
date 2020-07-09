from __future__ import annotations
from app import create_app
from app.model.database import db
from app.model.sandbox import add_dummy_objects, results, benchmarks, sites, tags, uploaders
from app.model.data_types import Uploader, Tag, Result, Benchmark, Site, ResultIterator
from app.model.facade import facade
import code

# utility helpers for functions not part of design
def get_uploaders() -> List[Uploader]:
    """Get all uploaders."""
    # prepare query
    return db.session.query(Uploader).all()

def get_benchmarks() -> List[Benchmark]:
    """Get all benchmarks."""
    # prepare query
    return db.session.query(Benchmark).all()

app = create_app()

add_dummy_objects(app)

code.interact(local=locals())
