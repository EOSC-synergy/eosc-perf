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


def email_updated(user):
    return EmailMessage(
        subject="Your email was updated",
        body="Thank you for updating your information.",
        from_email=current_app.config['MAIL_FROM'],
        to=[user.email]
    ).send()


def resource_submitted(resource):
    resource_type = resource.submit_report.resource_type
    return EmailMessage(
        subject=f"New {resource_type} resource submitted: {resource.id}",
        headers={'Resource-ID': f"{resource.id}"},
        from_email=current_app.config['MAIL_FROM'],
        to=[resource.uploader.email],
        cc=[current_app.config['MAIL_SUPPORT']],
        body=f"""
        Your resource was successfully submitted, our administrators now will
        review the data to accept it into our system.

        resource: {resource.id}
        """,
    ).send()


def resource_approved(resource):
    return EmailMessage(
        subject=f"Resource approved: {resource.id}",
        headers={'Resource-ID': f"{resource.id}"},
        from_email=current_app.config['MAIL_FROM'],
        to=[resource.uploader.email],
        cc=[current_app.config['MAIL_SUPPORT']],
        body=f"""
        Your resource was approved by our administrators. Now it will be
        displayed by default methods in our system.

        resource: {resource.id}
        """,
    ).send()


def resource_rejected(resource):
    return EmailMessage(
        subject=f"Resource rejected: {resource.id}",
        headers={'Resource-ID': f"{resource.id}"},
        from_email=current_app.config['MAIL_FROM'],
        to=[resource.uploader.email],
        cc=[current_app.config['MAIL_SUPPORT']],
        body=f"""
        Your resource was rejected by our administrators. Please check the
        submitted information and do not hesitate to contact
        {current_app.config['MAIL_SUPPORT']} for more details.

        resource: {resource.id}
        """,
    ).send()


def result_claimed(result, claim):
    return EmailMessage(
        subject=f"Claim submitted on result: {result.id}",
        headers={'Result-ID': f"{result.id}", 'Claim-ID': f"{claim.id}"},
        from_email=current_app.config['MAIL_FROM'],
        to=[result.uploader.email],
        cc=[current_app.config['MAIL_SUPPORT']],
        body=f"""
        Your resource was claimed by a community users. It will be temporary
        hidden from our list of results and reviewed by our administrators

        If the claim is valid the result might be permanently deleted.

        result: {result.id}
        claim: {claim.id}
        """,
    ).send()


def result_restored(result):
    return EmailMessage(
        subject=f"Result restored: {result.id}",
        headers={'Result-ID': result.id},
        from_email=current_app.config['MAIL_FROM'],
        to=[result.uploader.email],
        cc=[current_app.config['MAIL_SUPPORT']],
        body=f"""
        Your result was restored.

        result: {result.id}
        """,
    ).send()
