# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: Python [conda env:bedmap2]
#     language: python
#     name: conda-env-bedmap2-py
# ---

# # Transform Bedmap2 data given as GeoTiff files to netCDF files
#
# **Reference:**
#
# - Fretwell, P. et al. (2013). Bedmap2: improved ice bed, surface and thickness datasets for Antarctica. The Cryosphere. doi:10.5194/tc-7-375-2013

# Import libraries

import pooch
import xarray as xr
from pathlib import Path

# Define directories where the original data will be downloaded and where the netCDF files will be saved

# +
results_dir = Path(".") / "results"
data_dir = Path(".") / "data"

# Create results dir if it doesn't exists
results_dir.mkdir(exist_ok=True)
# -

# Initialize a Pooch instance with the url and registry for downloading Bedmap2 data

POOCH = pooch.create(
    path=data_dir,
    base_url="https://secure.antarctica.ac.uk/data/bedmap2/",
    registry={
        "bedmap2_tiff.zip": "f4bb27ce05197e9d29e4249d64a947b93aab264c3b4e6cbf49d6b339fb6c67fe",
    },
)

# Define a dictionary with the name of the datasets provided by Bedmap2

datasets = {
    "bed": dict(name="Bedrock Height", units="meters"),
    "surface": dict(name="Ice Surface Height", units="meters"),
    "thickness": dict(name="Ice Thickness", units="meters"),
    "icemask_grounded_and_shelves": dict(
        name="Mask of Grounding Line and Floating Ice Shelves"
    ),
    "rockmask": dict(name="Mask of Rock Outcrops"),
    "lakemask_vostok": dict(name="Mask for Lake Vostok"),
    "grounded_bed_uncertainty": dict(name="Ice Bed Uncertainty", units="meters"),
    "thickness_uncertainty_5km": dict(name="Ice Thickness Uncertainty", units="meters"),
    "coverage": dict(name="Distribution of Ice Thickness Data (binary)"),
    "geoid": dict(name="Geoid Height (WGS84)", units="meters"),
}


# Define function useful for getting the name of the GeoTiff file for the desired dataset

def get_fname(dataset, fnames):
    "Return the file name corresponding to the given dataset"
    if dataset == "geoid":
        dataset_name = "gl04c_geiod_to_WGS84.tif"
    else:
        dataset_name = "bedmap2_{}.tif".format(dataset)
    result = None
    for fname in fnames:
        if Path(fname).name == dataset_name:
            result = fname
    return result


# Fetch Bedmap2 original data

fnames = POOCH.fetch("bedmap2_tiff.zip", processor=pooch.Unzip())

# Build two datasets: `grid` and `uncertainty`.
#
# - The `grid` is a `xarray.Dataset` containing all the datasets provided by Bedmap2 except for `thickness_uncertainty_5km`, which is defined on a different set of points.
#
# - The `uncertainty` is a `xarray.Dataset` containing only the `thickness_uncertainty_5km` data.

# +
arrays = []
for dataset in datasets:
    # Read the geotiff files using rasterio
    array = xr.open_rasterio(get_fname(dataset, fnames))
    # Remove "band" dimension and coordinate
    array = array.squeeze("band", drop=True)
    # Set a name for this dataarray
    array.name = dataset
    array.attrs["long_name"] = datasets[dataset]["name"]
    # Append units for the x and y coordinates, and for the array if needed
    array.x.attrs["units"] = "meters"
    array.y.attrs["units"] = "meters"
    if "units" in datasets[dataset]:
        array.attrs["units"] = datasets[dataset]["units"]
    
    
    if dataset != "thickness_uncertainty_5km":
        # Append array to arrays list
        arrays.append(array)
    else:
        # Convert the thickness_uncertainty_5km to its own xarray.Dataset
        uncertainty = array.to_dataset()

# Merge arrays list into a single xarray.Dataset
grid = xr.merge(arrays)
# Remove arrays list for saving some memory
del arrays
# Add metadata to both datasets
metadata = {
    "title": "Bedmap2",
    "projection": "Antarctic Polar Stereographic",
    "true_scale_latitude": -71,
    "datum": "WGS84",
    "EPSG": "3031",
    "doi": "10.5194/tc-7-375-2013",
}
grid.attrs.update(metadata)
uncertainty.attrs.update(metadata)
# -

grid

uncertainty

# Save datasets as netCDF files.
#
# Use `zlib` encoding for reducing their size.

grid.bed

grid.to_netcdf(
    results_dir / "bedmap2.nc",
    encoding={dataset: {"zlib": True} for dataset in grid},
)
uncertainty.to_netcdf(
    results_dir / "bedmap2_ice_uncertainty.nc",
    encoding={dataset: {"zlib": True} for dataset in uncertainty},
)
