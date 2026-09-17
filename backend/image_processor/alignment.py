import rasterio
from rasterio.warp import reproject, Resampling

def align_image(source_path, reference_path, output_path):

    with rasterio.open(reference_path) as reference:

        with rasterio.open(source_path) as source:

            profile = reference.profile.copy()

            profile.update(
                width=reference.width,
                height=reference.height,
                transform=reference.transform,
                crs=reference.crs
            )

            with rasterio.open(output_path, "w", **profile) as destination:

                reproject(
                    source=rasterio.band(source, 1),
                    destination=rasterio.band(destination, 1),
                    src_transform=source.transform,
                    src_crs=source.crs,
                    dst_transform=reference.transform,
                    dst_crs=reference.crs,
                    resampling=Resampling.bilinear
                )