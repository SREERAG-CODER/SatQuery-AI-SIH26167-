import rasterio

def get_metadata(image_path):
    with rasterio.open(image_path) as src:
        metadata={
            "file": image_path,
            "width": src.width,  
            "height":src.height,
            "crs":str(src.crs),  # Coordinate Reference System --> tells us how pixel location corresponds to real-world coordinates
            "resolution":src.res, # How much real-world distance each pixel represents
            "bounds":{ # Geographical extent of the image in real-world coordinates
                "left":src.bounds.left,
                "top":src.bounds.top,
                "right":src.bounds.right,
                "bottom":src.bounds.bottom
            },
            "band_count":src.count, #How many bands (layers) the image has, e.g., RGB images have 3 bands   
            "bands":[],
            "nodata":src.nodata
        }

        for i in range(1, src.count + 1):
            band = src.tags(i)  # Get metadata for each band
            metadata["bands"].append({
                "band_number": i,
                "description": band.get("DESCRIPTION", f"band {i}"),  # Get description if available, else default to "band {i}"

            })

        return metadata

