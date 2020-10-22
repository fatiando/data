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
#     display_name: Python [conda env:rockhound-data]
#     language: python
#     name: conda-env-rockhound-data-py
# ---

# # Transform Bedmap2 data given as GeoTiff files to netCDF files
#
# **Reference:**
#
# - Fretwell, P. et al. (2013). Bedmap2: improved ice bed, surface and thickness datasets for Antarctica. The Cryosphere. doi:10.5194/tc-7-375-2013

# Import libraries

import pooch
import numpy as np
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
    "bed": dict(
        name="Bedrock Height",
        description="Height of bedrock relative to sea level as defined by the G104C geoid.",
        units="meters",
    ),
    "surface": dict(
        name="Ice Surface Height",
        description="Height of ice surface relative to sea level as defined by the G104C geoid.",
        units="meters",
    ),
    "thickness": dict(
        name="Ice Thickness",
        description="Thickness of the ice sheet.",
        units="meters",
    ),
    "icemask_grounded_and_shelves": dict(
        name="Mask of Grounding Line and Floating Ice Shelves",
    ),
    "rockmask": dict(name="Mask of Rock Outcrops"),
    "lakemask_vostok": dict(name="Mask for Lake Vostok"),
    "bed_uncertainty": dict(
        name="Ice Bed Uncertainty",
        description="Uncertainty of the bedrock height",
        units="meters",
    ),
    "thickness_uncertainty_5km": dict(
        name="Ice Thickness Uncertainty",
        description="Uncertainty of ice thickness on a grid with spacing of 5km.",
        units="meters",
    ),
    "coverage": dict(
        name="Distribution of Ice Thickness Data",
        description="Distribution of ice thickness data used to grid the ice thickness.",
    ),
    "geoid": dict(
        name="G104C Geoid Height",
        description="Height of the G104C Geoid relative to the WGS84 datum.",
        units="meters",
    ),
}


# Define function useful for getting the name of the GeoTiff file for the desired dataset


def get_fname(dataset, fnames):
    "Return the file name corresponding to the given dataset"
    if dataset == "geoid":
        tif_file = "gl04c_geiod_to_WGS84.tif"
    elif dataset == "bed_uncertainty":
        tif_file = "bedmap2_grounded_bed_uncertainty.tif"
    else:
        tif_file = "bedmap2_{}.tif".format(dataset)
    (fname,) = [f for f in fnames if Path(f).name == tif_file]
    return fname


# Fetch Bedmap2 original data

fnames = POOCH.fetch("bedmap2_tiff.zip", processor=pooch.Unzip())

# ## Load Bedmap2 data as xarray.Dataset

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

    # Replace no data values with nans
    # Filling with nans converts arrays to float64.
    # We will convert them first to float32 to avoid large memory consumption.
    # (float32 is enough to represent the given data).
    array = array.astype("float32")
    if dataset == "grounded_bed_uncertainty":
        # On grounded_bed_uncertainty the nodatavals is wrongly set to nan
        # but it should be its maximum value (~65000 meters).
        nan_value = array.max()
    else:
        nan_value = array.nodatavals
    array = array.where(array != nan_value)

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
# -

# Display generated xr.Datasets

grid

uncertainty

# ## Merge both datasets

# Incorporate the 5km coordinates into the main Dataset

# +
grid.coords["x_5km"] = ("x_5km", uncertainty.x.values)
grid.coords["y_5km"] = ("y_5km", uncertainty.y.values)

grid.x_5km.attrs = uncertainty.x.attrs
grid.y_5km.attrs = uncertainty.y.attrs
# -

# Add the thickness_uncertainty_5km array to the main Dataset

grid["thickness_uncertainty_5km"] = (
    ("y_5km", "x_5km"),
    uncertainty.thickness_uncertainty_5km,
)
grid.thickness_uncertainty_5km.attrs = uncertainty.thickness_uncertainty_5km.attrs

grid

# ## Tune dataset attributes

for dataset in grid:

    # Remove nodatavals, they are not needed anymore
    if "nodatavals" in grid[dataset].attrs:
        grid[dataset].attrs.pop("nodatavals")

    # Add actual_range attribute to each grid
    grid[dataset].attrs["actual_range"] = [
        np.nanmin(grid[dataset].values),
        np.nanmax(grid[dataset].values),
    ]

# +
history = ""

metadata = {
    "title": "Bedmap2",
    "institution": "British Antarctic Survey",
    "source": "Compiled from the GeoTiff files released by the British Antarctic Survey",
    "license": "unknown",
    "references": "https://doi.org/10.5194/tc-7-375-2013",
    "Conventions": "CF-1.8",
    "crs": "EPSG:3031",
    "datum": "WGS84",
    "projection": "Antarctic Polar Stereographic",
    "true_scale_latitude": -71,
    "history": history,
}
grid.attrs.update(metadata)
# -

grid

# ## Save dataset as netCDF file

# Configure encoding for each array in order to reduce the size of the netCDF file.

# +
encoding = {
    "bed": {"dtype": "int16", "_FillValue": -9_999},
    "surface": {"dtype": "int16", "_FillValue": -9_999},
    "thickness": {"dtype": "int16", "_FillValue": -9_999},
    "icemask_grounded_and_shelves": {"dtype": "int8", "_FillValue": -128},
    "rockmask": {"dtype": "int8", "_FillValue": -128},
    "lakemask_vostok": {"dtype": "int8", "_FillValue": -128},
    "bed_uncertainty": {"dtype": "uint16", "_FillValue": 9_999},
    "coverage": {"dtype": "int8", "_FillValue": -128},
    "geoid": {"dtype": "float32", "_FillValue": 9_999},
}

grid.to_netcdf(
    results_dir / "bedmap2.nc",
    encoding=encoding,
)
# -

grid = xr.open_dataset(results_dir / "bedmap2.nc")

grid
