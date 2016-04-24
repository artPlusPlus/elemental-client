import requests
import weakref

from elemental_core.util import process_elemental_class_value

# Imports are to trigger Resource class instantiation
from ._attribute_type import AttributeType
from ._content_type import ContentType
from ._attribute_instance import AttributeInstance
from ._content_instance import ContentInstance


_FMT_GET_RESOURCE = 'http://{0}:{1}/resources/{2}'.format


class Client(object):
    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def get_resource(self, resource_id):
        resource_data = self.pull_resource(resource_id)
        resource_type = resource_data['type']
        resource_id = resource_data['id']
        resource_type = process_elemental_class_value(resource_type)
        resource = resource_type(resource_id)
        resource.bind(weakref.proxy(self))

        return resource

    def pull_resource(self, resource_id):
        req = _FMT_GET_RESOURCE(self._host, self._port, resource_id)
        req = requests.get(req)

        if req.status_code != 200:
            raise RuntimeError(str(req.status_code))

        return req.json()
