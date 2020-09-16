from typing import List
import code
from app.flask_app import flask_app
from app.model.database import db
from app.model.sandbox import *
from app.model.data_types import *
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

code.interact(local=locals())
