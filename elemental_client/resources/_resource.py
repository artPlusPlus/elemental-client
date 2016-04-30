import logging
import uuid
import weakref

from elemental_core import ElementalBase
from elemental_core.util import process_uuid_value


_LOG = logging.getLogger(__name__)


class Resource(ElementalBase):
    @property
    def id(self):
        return self._id

    @property
    def connection(self):
        return self._connection

    def __init__(self, id=None):
        self._id = process_uuid_value(id) or uuid.uuid4()
        self._connection = None

    def bind_connection(self, connection):
        try:
            connection = weakref.proxy(connection)
        except TypeError:
            pass

        if connection == self._connection:
            return
        elif self._connection:
            self.unbind(self._connection)

        self._connection = connection
        self._connection.bind_resource(self)

    def unbind_connection(self, connection):
        try:
            connection = weakref.proxy(connection)
        except TypeError:
            pass

        if connection != self._connection:
            return

        self._connection = None
        connection.unbind_resource(self)
