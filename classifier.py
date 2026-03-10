import os

def detect_document_type(text):

    text = text.lower()

    schemas_folder = "schemas"

    for file in os.listdir(schemas_folder):

        if file.startswith("global_") and file.endswith(".json"):

            doc_type = file.replace("global_", "").replace("_document_schema.json","")

            if doc_type.replace("_"," ") in text or doc_type in text:
                return doc_type

    return "unknown"



