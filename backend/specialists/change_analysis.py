import rasterio
import numpy as np

def detect_change(before_path, after_path, output_path, threshold=0.5):

    with rasterio.open(before_path) as before:
        before_data = before.read(1)
        profile = before.profile.copy()

        with rasterio.open(after_path) as after:
            after_data = after.read(1)

            difference = np.abs(after_data - before_data)

            change_map = (difference > threshold).astype("uint8")

            profile.update(
                dtype="uint8",
                count=1
            )

            with rasterio.open(output_path, "w", **profile) as output:
                output.write(change_map, 1)

    changed_pixels = np.sum(change_map)
    total_pixels = change_map.size
    change_percentage = (changed_pixels / total_pixels) * 100

    return {
    "output": output_path,
    "threshold": threshold,
    "changed_pixels": int(changed_pixels),
    "change_percentage": float(change_percentage),
    "summary": f"Significant pixel-level differences were detected in approximately {change_percentage:.2f}% of the analyzed area."
    }