from six import itervalues

from flask.ext.marshmallow import Schema, base_fields
from marshmallow import validate


class Parameters(Schema):

    def __init__(self, api=None, **kwargs):
        super(Parameters, self).__init__(strict=True, **kwargs)


class JSONParameters(Parameters):
    """
    Base JSON parameters class forcing all fields to be in ``json``/``body``.
    """

    def __init__(self, *args, **kwargs):
        super(JSONParameters, self).__init__(*args, **kwargs)
        for field in itervalues(self.fields):
            field.metadata['location'] = 'json'


class PatchJSONParameters(JSONParameters):
    """
    Base parameters class for handling PATCH arguments according to RFC 6902.
    """

    # All operations described in RFC 6902
    OP_ADD = 'add'
    OP_REMOVE = 'remove'
    OP_REPLACE = 'replace'
    OP_MOVE = 'move'
    OP_COPY = 'copy'
    OP_TEST = 'test'

    # However, we use only those which make sense in RESTful API
    OPERATION_CHOICES = (
        OP_TEST,
        OP_ADD,
        OP_REMOVE,
        OP_REPLACE,
    )
    op = base_fields.String(required=True)

    PATH_CHOICES = None
    path = base_fields.String(required=True)

    value = base_fields.Raw(required=False)

    def __init__(self, *args, **kwargs):
        super(PatchJSONParameters, self).__init__(*args, many=True, **kwargs)
        if not self.PATH_CHOICES:
            raise ValueError("%s.PATH_CHOICES has to be set" % self.__class__.__name__)
        # Make a copy of `validators` as otherwise we will modify the behaviour
        # of all `marshmallow.Schema`-based classes
        self.fields['op'].validators = \
            self.fields['op'].validators + [validate.OneOf(self.OPERATION_CHOICES)]
        self.fields['path'].validators = \
            self.fields['path'].validators + [validate.OneOf(self.PATH_CHOICES)]
