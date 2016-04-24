import logging
import uuid
import weakref

from elemental_core import ElementalBase


_LOG = logging.getLogger(__name__)


class Resource(ElementalBase):
    @property
    def id(self):
        return self._id

    @property
    def client(self):
        return self._client

    def __init__(self, id=None):
        self._id = id or uuid.uuid4()
        self._client = None

    def bind(self, client):
        try:
            self._client = weakref.proxy(client)
        except TypeError:
            self._client = client
