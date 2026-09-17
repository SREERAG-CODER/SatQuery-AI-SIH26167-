from image_processor.metadata import get_metadata
from image_processor.validator import validate_metadata
from image_processor.inspector import inspect_inputs

image_path = "../data/Before/kochi_before.tif"

print("Available Metadata\n")
metadata = get_metadata(image_path)
print(metadata)

print("Validation Check")
validation = validate_metadata(metadata)
print(validation)

print("Input Inspection")
image_paths = ["../data/Before/kochi_before.tif"]
inspection_result = inspect_inputs(image_paths)
print(inspection_result)

