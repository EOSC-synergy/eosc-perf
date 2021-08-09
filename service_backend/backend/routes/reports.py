"""Report routes."""
from backend.extensions import auth
from backend.models import models
from backend.schemas import args, schemas
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    'reports', __name__, description='Operations on reports'
)


@blp.route('')
class Root(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='GetReports')
    @blp.arguments(args.ReportFilter, location='query', as_kwargs=True)
    @blp.response(200, schemas.Reports)
    def get(self, page=1, per_page=100, before=None, after=None, **kwargs):
        """Filters and list  reports."""
        query = models.Report.query.filter_by(**kwargs)
        if before:
            query = query.filter(models.Report.created_at < before)
        if after:
            query = query.filter(models.Report.created_at > after)

        return query.paginate(page, per_page)


@blp.route('/<uuid:report_id>')
class ReportId(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='GetReport')
    @blp.response(200, schemas.Report)
    def get(self, report_id):
        """Retrieves report details."""
        return models.Report.get(report_id)

    @auth.admin_required()
    @blp.doc(operationId='DelReport')
    @blp.response(204)
    def delete(self, report_id):
        """Deletes an existing report."""
        models.Report.get(report_id).delete()


@blp.route('/<uuid:report_id>/approve')
class Approve(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='ApproveReport')
    @blp.response(204)
    def patch(self, report_id):
        """Approves the indicated report id."""
        models.Report.get(report_id).update(verdict=True)


@blp.route('/<uuid:report_id>/reject')
class Reject(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='RejectReport')
    @blp.response(204)
    def patch(self, report_id):
        """Rejects the indicated report id."""
        models.Report.get(report_id).update(verdict=False)
