import copy

def adapt_schema(global_schema, country):

    schema = copy.deepcopy(global_schema)

    for field in schema:

        if isinstance(field, dict):

            # add country tag to field
            field["country_specific"] = country

            # check nested fields
            if "subFields" in field:

                for sub in field["subFields"]:
                    sub["country_specific"] = country

    return {
        "fields": schema
    }



