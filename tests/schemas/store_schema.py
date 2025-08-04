# schemas/store_schema.py

STORE_SCHEMA = {
    "type": "object",
    "required": ["id", "petId", "quantity", "status", "complete"],
    "properties": {
        "id": {"type": "integer"},
        "petId": {"type": "integer"},
        "quantity": {"type": "integer"},
        "status": {"type": "string"},
        "complete": {"type": "boolean"}
    }
}