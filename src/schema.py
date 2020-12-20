CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "sites": {
            "type": "array"
        }
    },
    "required": ["sites"]
}


STATUS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "httpStatus": {
            "type": "integer"
        },
        "responseTimeSeconds": {
            "type": "number"
        },
    },
    "required": ["httpStatus", "responseTimeSeconds"]
}
