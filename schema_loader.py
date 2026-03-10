import json
import os

def load_schema(doc_type):

    schema_file = f"schemas/global_{doc_type}_document_schema.json"

    if os.path.exists(schema_file):

        with open(schema_file, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    return []