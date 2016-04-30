import json as default_json


_json = default_json


def serialize_content_type(content_type):
    data = {
        'type': type(content_type).__name__,
        'id': str(content_type.id),
        'name': str(content_type.name),
        'base_ids': [str(base.id) for base in content_type.base_types],
        'attribute_type_ids': [str(at.id) for at in content_type.attribute_types]
    }

    data = _json.dumps(data)

    return data


def serialize_attribute_type(attribute_type):
    data = {
        'type': type(attribute_type).__name__,
        'id': str(attribute_type.id),
        'name': str(attribute_type.name),
        'default_value': attribute_type.default_value,
        'kind_id': attribute_type.kind.__name__ if attribute_type.kind else None,
        'kind_properties': attribute_type.kind_properties
    }

    data = _json.dumps(data)

    return data


def serialize_content_instance(content_instance):
    data = {
        'type': type(content_instance).__name__,
        'id': str(content_instance.id),
        'type_id': str(content_instance.type_id),
        'attribute_ids': [str(attr.id) for attr in content_instance.attributes]
    }

    data = _json.dumps(data)

    return data


def serialize_attribute_instance(attribute_instance):
    if attribute_instance.source:
        source_id = str(attribute_instance.source.id)
    else:
        source_id = attribute_instance.source

    data = {
        'type': type(attribute_instance).__name__,
        'id': str(attribute_instance.id),
        'type_id': str(attribute_instance.attribute_type.id),
        'value': attribute_instance.value,
        'source_id': source_id
    }

    data = _json.dumps(data)

    return data