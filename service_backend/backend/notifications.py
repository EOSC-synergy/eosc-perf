"""Module with notification definitions for users and admins."""
from functools import wraps

from flask import current_app
from flask_mailman import EmailMessage


def warning_if_fail(notification):
    @wraps(notification)
    def decorated(*args, **kwargs):
        try:
            return notification(*args, **kwargs)
        except Exception as err:
            current_app.logger.warning(f"{err}")
            return err

    return decorated


# -------------------------------------------------------------------
# User welcome ------------------------------------------------------
user_welcome_body = """
Dear user,

Your registration process is complete.
Thank you for using eosc-performance.

Best regards,
perf-support
"""


@warning_if_fail
def user_welcome(user):
    return EmailMessage(
        subject="Thank you for registering",
        body=user_welcome_body,
        from_email=current_app.config["MAIL_FROM"],
        to=[user.email],
    ).send()


# -------------------------------------------------------------------
# Email update ------------------------------------------------------
email_update_body = """
Dear user,

Your information update process is complete.
Thank you for using eosc-performance.

Best regards,
perf-support
"""


@warning_if_fail
def email_updated(user):
    return EmailMessage(
        subject="Your user information was updated",
        body=email_update_body,
        from_email=current_app.config["MAIL_FROM"],
        to=[user.email],
    ).send()


# -------------------------------------------------------------------
# Resource submitted ------------------------------------------------
resource_submitted_body = """
Dear user,

Your '{resource.__class__.__name__}' was successfully submitted,
our administrators now will review the data to accept it into our system.
Resource: {resource.id}

Thank you for using eosc-performance.

Best regards,
perf-support
"""


@warning_if_fail
def resource_submitted(resource):
    resource_type = resource.submit_report.resource_type
    return EmailMessage(
        subject=f"New {resource_type} resource submitted: {resource.id}",
        body=resource_submitted_body.format(resource=resource),
        headers={"Resource-ID": f"{resource.id}"},
        from_email=current_app.config["MAIL_FROM"],
        to=[resource.uploader.email],
        cc=[current_app.config["MAIL_SUPPORT"]],
    ).send()


# -------------------------------------------------------------------
# Resource approved -------------------------------------------------
resource_approved_body = """
Dear user,

Your '{resource.__class__.__name__}' has been approved by our administrators.
Resource: {resource.id}

Thank you for using eosc-performance.

Best regards,
perf-support
"""


@warning_if_fail
def resource_approved(resource):
    return EmailMessage(
        subject=f"Resource approved: {resource.id}",
        body=resource_approved_body.format(resource=resource),
        headers={"Resource-ID": f"{resource.id}"},
        from_email=current_app.config["MAIL_FROM"],
        to=[resource.uploader.email],
        cc=[current_app.config["MAIL_SUPPORT"]],
    ).send()


# -------------------------------------------------------------------
# Resource rejected -------------------------------------------------
resource_rejected_body = """
Dear user,

Unfortunately your '{resource.__class__.__name__}' has been rejected
by our administrators.
Please check the submitted information and do not hesitate to contact
resource: {resource.id}

Thank you for using eosc-performance.

Best regards,
perf-support
"""


@warning_if_fail
def resource_rejected(uploader, resource):
    return EmailMessage(
        subject=f"Resource rejected: {resource.id}",
        body=resource_rejected_body.format(resource=resource),
        headers={"Resource-ID": f"{resource.id}"},
        from_email=current_app.config["MAIL_FROM"],
        to=[uploader.email],
        cc=[current_app.config["MAIL_SUPPORT"]],
    ).send()


# -------------------------------------------------------------------
# Resource submitted ------------------------------------------------
result_claimed_body = """
Dear user,

Your result was claimed by a community users. It will be temporary
hidden from our list of results and reviewed by our administrators.

If the claim is valid the result might be permanently deleted.
result: {result.id}
claim: {claim.id}

Thank you for using eosc-performance.

Best regards,
perf-support
"""


@warning_if_fail
def result_claimed(result, claim):
    return EmailMessage(
        subject=f"Claim submitted on result: {result.id}",
        body=result_claimed_body.format(result=result, claim=claim),
        headers={"Result-ID": f"{result.id}", "Claim-ID": f"{claim.id}"},
        from_email=current_app.config["MAIL_FROM"],
        to=[result.uploader.email],
        cc=[current_app.config["MAIL_SUPPORT"]],
    ).send()


# -------------------------------------------------------------------
# Resource restored -------------------------------------------------
result_restored_body = """
Dear user,

Your result was reviewed by the administrators and restored.
Users can receive your result using our generic listing tools.
resource: {result.id}

Thank you for using eosc-performance.

Best regards,
perf-support
"""


@warning_if_fail
def result_restored(result):
    return EmailMessage(
        subject=f"Result restored: {result.id}",
        body=result_restored_body.format(result=result),
        headers={"Result-ID": result.id},
        from_email=current_app.config["MAIL_FROM"],
        to=[result.uploader.email],
        cc=[current_app.config["MAIL_SUPPORT"]],
    ).send()
