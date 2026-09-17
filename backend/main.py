from image_processor.inspector import inspect_inputs
from agent.router import route_query
from specialists.registry import SPECIALISTS

image_paths = ["data/Before/kochi_before.tif", "data/After/kochi_after_aligned.tif"]

query = "What changed between these two images?"

inspection = inspect_inputs(image_paths)

print("Input Inspection")
print(inspection)

task = route_query(query, inspection["input_type"])

print("Selected Task")
print(task)

if task in SPECIALISTS:
    specialist = SPECIALISTS[task]

    result = specialist(
        image_paths[0],
        image_paths[1],
        "data/change_map.tif"
    )

    print("Specialist Result")
    print(result)