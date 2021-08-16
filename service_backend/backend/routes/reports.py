"""Report routes."""
from backend import models
from backend.extensions import auth
from backend.schemas import args, schemas
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    'reports', __name__, description='Operations on reports'
)


@blp.route('')
class Root(MethodView):
    """Class defining the main endpoint methods for reports"""

    @auth.admin_required()
    @blp.doc(operationId='GetReports')
    @blp.arguments(args.ReportFilter, location='query')
    @blp.response(200, schemas.Reports)
    def get(self, query_args):
        """(Admins) Filters and list  reports

        Use this method to get a list of reports filtered according to your 
        requirements. The response returns a pagination object with the
        filtered reports (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered reports
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        per_page = query_args.pop('per_page')
        page = query_args.pop('page')
        query = models.Report.query

        # Extend query with date filter
        before = query_args.pop('before')
        if before:
            query = query.filter(models.Report.created_at < before)
        after = query_args.pop('after')
        if after:
            query = query.filter(models.Report.created_at > after)

        query = query.filter_by(**query_args)
        return query.paginate(page, per_page)


@blp.route('/<uuid:report_id>')
class ReportId(MethodView):
    """Class defining the specific report endpoint"""

    @auth.admin_required()
    @blp.doc(operationId='GetReport')
    @blp.response(200, schemas.Report)
    def get(self, report_id):
        """(Admins) Retrieves report details

        Use this method to retrieve a specific report from the database.
        ---

        If no report exists with the indicated id, then 404 NotFound
        exception is raised.        

        :param report_id: The id of the report to retrieve
        :type report_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No report with id found
        :return: The database report using the described id
        :rtype: :class:`models.Report`
        """
        return models.Report.get(report_id)

    @auth.admin_required()
    @blp.doc(operationId='DelReport')
    @blp.response(204)
    def delete(self, report_id):
        """(Admins) Deletes an existing report

        Use this method to delete a specific report from the database.
        ---

        If no report exists with the indicated id, then 404 NotFound
        exception is raised.        

        :param report_id: The id of the report to delete
        :type report_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No report with id found
        """
        models.Report.get(report_id).delete()


@blp.route('/<uuid:report_id>/approve')
class Approve(MethodView):
    """Class defining the endpoint to approve a report"""

    @auth.admin_required()
    @blp.doc(operationId='ApproveReport')
    @blp.response(204)
    def patch(self, report_id):
        """(Admins) Approves the indicated report id

        Use this method to approve a specific report from the database.
        ---

        If no report exists with the indicated id, then 404 NotFound
        exception is raised.        

        :param report_id: The id of the report to approve
        :type report_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No report with id found
        """
        models.Report.get(report_id).update(verdict=True)


@blp.route('/<uuid:report_id>/reject')
class Reject(MethodView):
    """Class defining the endpoint to reject a report"""

    @auth.admin_required()
    @blp.doc(operationId='RejectReport')
    @blp.response(204)
    def patch(self, report_id):
        """(Admins) Rejects the indicated report id

        Use this method to close a specific report from the database.
        ---

        If no report exists with the indicated id, then 404 NotFound
        exception is raised.        

        :param report_id: The id of the report to close
        :type report_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No report with id found
        """
        models.Report.get(report_id).update(verdict=False)
