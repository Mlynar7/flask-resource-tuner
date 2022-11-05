from schema import Schema, SchemaError


def validate_schema(schema: Schema, data: dict):
    try:
        d = schema.validate(data)
    except SchemaError as e:
        return {}, str(e.autos)
    else:
        return d, []
