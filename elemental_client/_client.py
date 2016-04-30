from ._connection import Connection


class Client(object):
    @property
    def host(self):
        return self._connection.host

    @property
    def port(self):
        return self._connection.port

    def __init__(self, host, port):
        self._connection = Connection(host, port)

    def create_resource(self, resource_type):
        return self._connection.create_resource(resource_type)

    def retrieve_resource(self, resource_id):
        return self._connection.get_resource(resource_id)

    def delete_resource(self, resource):
        self._connection.delete_resource(resource)
