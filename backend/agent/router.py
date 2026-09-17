def route_query(query, input_type):

    query = query.lower()

    if input_type == "pair":
        if "change" in query or "changed" in query or "difference" in query:
            return "change"
        if "sar" in query or "optical" in query:
            return "optical_sar"

    if "where" in query or "location" in query or "region" in query:
        return "grounding"

    if "describe" in query or "caption" in query or "scene" in query:
        return "captioning"

    return "vqa"