def process_inbound_resource_list_data(client, resource_list_data):
    resource_list_data = resource_list_data or []
    return [client.get_resource(resource_id) for resource_id in resource_list_data]


def process_outbound_resource_list_data(resource_list_data):
    result = []

    resource_list_data = resource_list_data or []
    if not isinstance(resource_list_data, (list, set, tuple)):
        resource_list_data = [resource_list_data]

    for resource_data in resource_list_data:
        if not resource_data:
            continue

        try:
            result.append(resource_data.id)
        except AttributeError:
            result.append(resource_data)

    return [str(resource_id) for resource_id in result]
