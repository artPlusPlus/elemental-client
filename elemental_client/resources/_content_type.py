import logging

from ._resource import Resource
from .._remote_value import RemoteValue
from .._util import (
    process_inbound_resource_list_data,
    process_outbound_resource_list_data
)

_LOG = logging.getLogger(__name__)


class ContentType(Resource):
    name = RemoteValue('name', default='UNNAMED_CONTENT_TYPE')
    base_types = RemoteValue('base_ids', default=[])

    @base_types.on_get
    def base_types(self, base_ids):
        return process_inbound_resource_list_data(self._client, base_ids)

    @base_types.on_set
    def base_types(self, base_types_data):
        return process_outbound_resource_list_data(base_types_data)

    attribute_types = RemoteValue('attribute_type_ids', default=[])

    @attribute_types.on_get
    def attribute_types(self, attribute_type_ids):
        return process_inbound_resource_list_data(self._client, attribute_type_ids)

    @attribute_types.on_set
    def attribute_types(self, attribute_types_data):
        return process_outbound_resource_list_data(attribute_types_data)
