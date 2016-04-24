import logging

from ._resource import Resource
from ._remote_value import RemoteValue
from ._util import (
    process_inbound_resource_list_data,
    process_outbound_resource_list_data
)


_LOG = logging.getLogger(__name__)


class ContentInstance(Resource):
    attributes = RemoteValue('attribute_ids')

    @attributes.on_get
    def attributes(self, attribute_data):
        return process_inbound_resource_list_data(self._client, attribute_data)

    @attributes.on_set
    def attributes(self, attribute_data):
        return process_outbound_resource_list_data(attribute_data)
