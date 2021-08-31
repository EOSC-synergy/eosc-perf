"""Module with notification definitions for users and admins."""
from flask import current_app
from flask_mailman import EmailMessage


def user_welcome(user):
    return EmailMessage(
        subject="Thank you for registering",
        body="Your registration process is complete.",
        from_email=current_app.config['MAIL_FROM'],
        to=[user.email]
    ).send()


def report_created(report):
    return EmailMessage(
        subject=f"New {report.resource_type} report: {report.id}",
        headers={'Report-ID': report.id, 'Report-verdict': report.verdict},
        body=report.message,
        from_email=current_app.config['MAIL_FROM'],
        to=[report.resource.uploader.email],
        cc=[current_app.config['MAIL_SUPPORT']],
    ).send()


def report_updated(report):
    if report.verdict == True:
        report_action = "approved"
    if report.verdict == False:
        report_action = "rejected"
    return EmailMessage(
        subject=f"Report {report_action}: {report.id}",
        headers={'Report-ID': report.id, 'Report-verdict': report.verdict},
        body=f"Report status was updated by an admin",
        from_email=current_app.config['MAIL_FROM'],
        to=[report.resource.uploader.email],
        cc=[current_app.config['MAIL_SUPPORT']],
    ).send()
