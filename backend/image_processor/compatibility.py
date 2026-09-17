def check_compatibility(metadata1, metadata2):

    result = {
        "compatible": True,
        "alignment_needed": False,
        "checks": []
    }

    if metadata1["crs"] != metadata2["crs"]:
        result["compatible"] = False
        result["checks"].append("CRS does not match.")
    else:
        result["checks"].append("CRS matches.")

    if metadata1["resolution"] != metadata2["resolution"]:
        result["alignment_needed"] = True
        result["checks"].append("Resolution does not match.")
    else:
        result["checks"].append("Resolution matches.")

    if metadata1["width"] != metadata2["width"] or metadata1["height"] != metadata2["height"]:
        result["alignment_needed"] = True
        result["checks"].append("Image dimensions do not match.")
    else:
        result["checks"].append("Image dimensions match.")

    if result["alignment_needed"] and result["compatible"]:
        result["checks"].append("Images require spatial alignment before comparison.")

    return result