from image_processor.metadata import get_metadata
from image_processor.validator import validate_metadata


def inspect_inputs(image_paths):

    result = {
        "image_count": len(image_paths),
        "images": [],
        "input_type": None
    }

    for image_path in image_paths:

        metadata = get_metadata(image_path)
        validation = validate_metadata(metadata)

        result["images"].append({
            "file": image_path,
            "valid": validation["valid"],
            "errors": validation["errors"]
        })

    # Determine input type
    if len(image_paths) == 1:
        result["input_type"] = "single"

    elif len(image_paths) == 2:
        result["input_type"] = "pair"

    else:
        result["input_type"] = "unsupported"

    return result