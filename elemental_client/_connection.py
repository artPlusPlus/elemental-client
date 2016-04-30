import weakref

import requests

from elemental_core.util import process_elemental_class_value

from .resources import *
from .serialization.json import *


_FMT_POST_URL = 'http://{0}:{1}/{2}'.format
_FMT_GET_URL = 'http://{0}:{1}/resources/{2}'.format
_FMT_PUT_URL = 'http://{0}:{1}/resources/{2}'.format
_FMT_DELETE_URL = 'http://{0}:{1}/resources/{2}'.format


_MAP_TYPE_SERIALIZER = {
    AttributeType: serialize_attribute_type,
    ContentType: serialize_content_type,
    AttributeInstance: serialize_attribute_instance,
    ContentInstance: serialize_content_instance
}


class Connection(object):
    _instances = {}
    _host = None
    _port = None
    _resources = None

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def __new__(cls, host, port):
        try:
            result = cls._instances[(host, port)]
        except KeyError:
            result = super(Connection, cls).__new__(cls)
            result.__init__(host, port)
            cls._instances[(host, port)] = result

        return weakref.proxy(result)

    def __init__(self, host, port):
        super(Connection, self).__init__()

        if (host, port) == (self._host, self._port):
            return

        self._host = host
        self._port = port
        self._resources = {}

    def create_resource(self, resource_type):
        resource_type = process_elemental_class_value(resource_type)
        resource = resource_type()

        self.bind_resource(resource)

        return weakref.proxy(resource)

    def _post_resource(self, resource):
        serializer = _MAP_TYPE_SERIALIZER.get(type(resource))
        if not serializer:
            raise RuntimeError()
        data = serializer(resource)
        req = _FMT_POST_URL(self._host, self._port, type(resource).__name__)
        resp = requests.post(req, data=data)

        if resp.status_code != 201:
            raise RuntimeError(str(resp.status_code))

    def get_resource(self, resource_id):
        try:
            result = self._resources[resource_id]
        except KeyError:
            resource_data = self.get_resource_data(resource_id)
            resource_type = resource_data['type']
            resource_type = process_elemental_class_value(resource_type)
            resource_id = resource_data['id']
            resource = resource_type(resource_id)

            self.bind_resource(resource)

            result = resource

        return weakref.proxy(result)

    def get_resource_data(self, resource_id):
        req = _FMT_GET_URL(self._host, self._port, resource_id)
        resp = requests.get(req)

        if resp.status_code != 200:
            raise RuntimeError(str(resp.status_code))

        return resp.json()

    def put_resource_data(self, resource_id, resource_data):
        req = _FMT_PUT_URL(self._host, self._port, resource_id)
        resp = requests.put(req, json=resource_data)

        if resp.status_code != 204:
            raise RuntimeError(str(resp.status_code))

    def delete_resource(self, resource):
        req = _FMT_DELETE_URL(self._host, self._port, resource.id)
        resp = requests.delete(req)

        if resp.status_code != 204:
            raise RuntimeError(str(resp.status_code))

    def bind_resource(self, resource):
        if resource.id in self._resources:
            return

        self._resources[resource.id] = resource
        resource.bind_connection(self)

        try:
            self.get_resource_data(resource.id)
        except RuntimeError:  # TODO: needs to look for a 404
            self._post_resource(resource)

    def unbind_resource(self, resource):
        try:
            del self._resources[resource.id]
        except KeyError:
            pass
        else:
            resource.unbind_connection(self)
