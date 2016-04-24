from elemental_core.util import process_elemental_class_value

from elemental_kinds import *  # Instantiation of AttributeKind classes

from ._resource import Resource
from ._remote_value import RemoteValue


class AttributeType(Resource):
    name = RemoteValue('name')
    default_value = RemoteValue('default_value')
    kind_id = RemoteValue('kind_id')
    kind_properties = RemoteValue('kind_properties')

    @property
    def kind(self):
        if not self.kind_id:
            return None

        return process_elemental_class_value(self.kind_id)
