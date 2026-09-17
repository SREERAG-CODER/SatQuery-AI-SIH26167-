def validate_metadata(metadata):

    result = {
    "valid": True,
    "errors": []
    }

    if metadata["crs"] is None:
        result["valid"] = False
        result["errors"].append("Image Has No CRS")

    if metadata["width"] <= 0 or metadata["height"] <= 0:
        result["valid"] = False
        result["errors"].append("Image Has Invalid Dimensions")

    if metadata["band_count"] <= 0:
        result["valid"] = False
        result["errors"].append("Image Has No Bands")

    return result
