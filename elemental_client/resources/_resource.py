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
    def client(self):
        return self._client

    def __init__(self, id=None):
        self._id = process_uuid_value(id) if id else uuid.uuid4()
        self._client = None

    def bind(self, client):
        try:
            client = weakref.proxy(client)
        except TypeError:
            pass

        if client == self._client:
            return
        elif self._client:
            self.unbind(self._client)

        self._client = client
        self._client.bind(self)

    def unbind(self, client):
        try:
            client = weakref.proxy(client)
        except TypeError:
            pass

        if client != self._client:
            return

        self._client = None
        client.unbind(self)
