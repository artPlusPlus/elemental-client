import logging

from ._resource import Resource
from .._remote_value import RemoteValue


_LOG = logging.getLogger(__name__)


class AttributeInstance(Resource):
    attribute_type = RemoteValue('type_id')

    @attribute_type.on_get
    def attribute_type(self, type_id):
        return self._connection.get_resource(type_id)

    @attribute_type.on_set
    def attribute_type(self, value):
        try:
            return value.id
        except AttributeError:
            return value

    value = RemoteValue('value')

    @value.on_get
    def value(self, value):
        source = self.source
        if source:
            return source.value
        return value

    @value.on_set
    def value(self, value):
        attr_type = self.attribute_type

        if attr_type:
            kind = attr_type.kind
            if kind:
                value = kind.process_value(value, **attr_type.kind_properties)
                kind.validate_value(value)
            else:
                msg = (
                    'AttributeInstance "{0}" value set without AttributeKind '
                    'processing or validation: AttributeKind "{1}" from '
                    'AttributeType "{2}" not resolved.'
                )
                msg = msg.format(self.id, attr_type.kind_id, attr_type.id)
                _LOG.warn(msg)
        else:
            msg = (
                'AttributeInstance "{0}" value set without AttributeKind '
                'processing or validation: AttributeType "{1}" not resolved.'
            )
            msg = msg.format(self.id, self.type_id)
            _LOG.debug(msg)

        return value

    source = RemoteValue('source_id')

    @source.on_get
    def source(self, source_id):
        return self._connection.get_resource(source_id)

    @source.on_set
    def source(self, source):
        try:
            return source.id
        except AttributeError:
            return source
