class RemoteValue(object):
    def __init__(self, label, doc=None, default=None):
        self.label = label
        self.doc = doc
        self.default = default
        self.get_handler = None
        self.set_handler = None

    def __call__(self, on_get=None, on_set=None):
        self.get_handler = on_get
        self.set_handler = on_set

        return self

    def __get__(self, resource, owner=None):
        if resource is None:
            return self

        connection = resource.connection
        if not connection:
            raise AttributeError('Unable to get value: no connection')

        try:
            resource_data = connection.get_resource_data(resource.id)
        except RuntimeError:
            resource_data = {}

        resource_data = resource_data.get(self.label, self.default)

        if self.get_handler:
            resource_data = self.get_handler(resource, resource_data)

        return resource_data

    def __set__(self, resource, value):
        connection = resource.connection
        if not connection:
            raise AttributeError('Unable to set value: no connection')

        resource_data = connection.get_resource_data(resource.id)

        if self.set_handler:
            resource_data[self.label] = self.set_handler(resource, value)
        else:
            resource_data[self.label] = value

        connection.put_resource_data(resource.id, resource_data)

    def on_get(self, get_handler):
        result = type(self)(self.label, doc=self.doc)
        result = result(on_get=get_handler, on_set=self.set_handler)
        return result

    def on_set(self, set_handler):
        result = type(self)(self.label, doc=self.doc)
        result = result(on_get=self.get_handler, on_set=set_handler)
        return result
