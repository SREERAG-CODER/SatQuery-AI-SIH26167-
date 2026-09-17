from image_processor.metadata import get_metadata
from image_processor.validator import validate_metadata
from image_processor.modality import identify_modality
from image_processor.compatibility import check_compatibility

def inspect_inputs(image_paths):

    result = {
        "image_count": len(image_paths),
        "images": [],
        "input_type": None,
        "compatibility": None
    }

    metadata_list = []

    for image_path in image_paths:
        metadata = get_metadata(image_path)
        validation = validate_metadata(metadata)
        modality = identify_modality(metadata)

        metadata_list.append(metadata)

        result["images"].append({
            "file": image_path,
            "valid": validation["valid"],
            "errors": validation["errors"],
            "modality": modality
        })

    if len(image_paths) == 1:
        result["input_type"] = "single"

    elif len(image_paths) == 2:
        result["input_type"] = "pair"

        result["compatibility"] = check_compatibility(
            metadata_list[0],
            metadata_list[1]
        )

    else:
        result["input_type"] = "unsupported"

    return result