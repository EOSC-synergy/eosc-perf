"""Schemas module with custom fields."""
import uuid

from marshmallow.fields import (UUID, Boolean, Date, DateTime, Dict, Email,
                                Integer, List, Nested, String)
from marshmallow.validate import OneOf


class Id(UUID):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "UUID resource unique identification"
        kwargs['example'] = str(uuid.uuid4())
        super().__init__(*args, **kwargs)


class Ids(List):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "List of UUID unique identifications"
        kwargs['example'] = [str(uuid.uuid4()) for _ in range(2)]
        super().__init__(Id(), *args, missing=[], **kwargs)


class Sub(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "String containing an OIDC subject"
        kwargs['example'] = "NzbLsXh8uDCcd-6MNwXF4W_7noWXFZAfHkxZsRGC9Xs"
        super().__init__(*args, **kwargs)


class Iss(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "String containing an OIDC issuer"
        kwargs['example'] = "https://self-issued.me"
        super().__init__(*args, **kwargs)


class Email(Email):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "Email of user collected by the OIDC token"
        kwargs['example'] = "simple_email@gmail.com"
        super().__init__(*args, **kwargs)


class DockerImage(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "String with a docker hub container name"
        kwargs['example'] = "deephdc/deep-oc-benchmarks_cnn"
        super().__init__(*args, **kwargs)


class DockerTag(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "String with a docker hub container tag"
        kwargs['example'] = "1.0.2-gpu"
        super().__init__(*args, **kwargs)


class JsonTemplate(Dict):
    def __init__(self, *args, **kwargs):
        # kwargs['description'] = description   # Does not work
        # kwargs['example'] = {},   # TODO: Add valid example
        super().__init__(*args, **kwargs)


class Verdict(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "Parameter describing the report status"
        kwargs['example'] = "null"
        kwargs['validate'] = OneOf(["true", "false", "null"])
        super().__init__(*args, **kwargs)


class Resource(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "Resource type discriminator"
        kwargs['example'] = "benchmark"
        kwargs['validate'] = OneOf(["benchmark", "result", "site", "flavor"])
        super().__init__(*args, **kwargs)


class UploadBefore(Date):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "Results with upload before date (ISO8601)"
        kwargs['example'] = "2059-03-10"
        super().__init__(*args, **kwargs)


class UploadAfter(Date):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "Results with upload after date (ISO8601)"
        kwargs['example'] = "2019-09-07"
        super().__init__(*args, **kwargs)


class SiteName(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "String with human readable institution identification"
        kwargs['example'] = "Karlsruhe Institute of Technology"
        super().__init__(*args, **kwargs)


class Address(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "String with place where a site is located"
        kwargs['example'] = "76131 Karlsruhe, Germany"
        super().__init__(*args, **kwargs)


class FlavorName(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "String with virtual hardware template identification"
        kwargs['example'] = "c6g.medium"
        super().__init__(*args, **kwargs)


class TagName(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "String with short feature identification"
        kwargs['example'] = "python"
        super().__init__(*args, **kwargs)


class TagNames(List):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "List of tag names"
        kwargs['example'] = ["python", "hpc"]
        super().__init__(TagName(), *args, missing=[], **kwargs)


class Description(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "String with an statement about the object"
        kwargs['example'] = "This is a simple description example"
        super().__init__(*args, **kwargs)


class Term(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "Subset expression of a string"
        kwargs['example'] = "search_term"
        super().__init__(*args, **kwargs)


class Terms(List):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "List of terms (string subsets)"
        kwargs['example'] = ["search_term 1", "search_term 2"]
        super().__init__(Term(), *args, missing=[], **kwargs)


class Filter(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "JSON filter condition (space sparated)"
        kwargs['example'] = "machine.cpu.count > 4"
        super().__init__(*args, **kwargs)


class Filters(List):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "List of filter conditions (space separated)"
        kwargs['example'] = ["machine.cpu.count > 4", "machine.cpu.count < 80"]
        super().__init__(Filter(), *args, missing=[], **kwargs)


class Message(String):
    def __init__(self, *args, **kwargs):
        kwargs['description'] = "Message included in a report"
        kwargs['example'] = "Result does not match benchmark template"
        super().__init__(*args, **kwargs)
