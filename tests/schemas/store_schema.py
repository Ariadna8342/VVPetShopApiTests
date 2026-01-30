INVENTORY_SCHEMA = {
    "type": "object",
    "properties":{
        "approved": {
            "type": "integer"
        },
        "delivered": {
            "type": "integer"
        },
        "status": {
            "type": "string"
        }
    },
    "required": ["approved"]
}

STORE_SCHEMA = {
    "type": "object",
    "properties":{
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"
        },
        "quantity": {

        },
        "status": {
            "type": "string"
        },
        "complete": {
            "type": "boolean"
        }
    },
    "required": ["id", "petId", "quantity", "status"]
}