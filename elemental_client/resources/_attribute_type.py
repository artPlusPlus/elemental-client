from elemental_core.util import process_elemental_class_value

import elemental_kinds

from ._resource import Resource
from .._remote_value import RemoteValue


class AttributeType(Resource):
    name = RemoteValue('name')
    default_value = RemoteValue('default_value')
    kind_properties = RemoteValue('kind_properties', default={})

    kind = RemoteValue('kind_id')

    @kind.on_get
    def kind(self, kind_id):
        if not kind_id:
            return None
        return process_elemental_class_value(kind_id)

    @kind.on_set
    def kind(self, value):
        if issubclass(value, elemental_kinds.AttributeKind):
            return value.__name__
        value_kind = process_elemental_class_value(value)
        if value_kind and issubclass(value_kind, elemental_kinds.AttributeKind):
            return value.__name__
        else:
            raise AttributeError('{0} is not a valid AttributeKind.')
