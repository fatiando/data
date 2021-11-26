# Contributing Guidelines

:tada: **First off, thank you for considering contributing to our project!** :tada:

This is a community-driven project, so it's people like you that make it useful and
successful.

If you get stuck at any point you can create an issue on GitHub (look for the *Issues*
tab in the repository) or contact us at one of the other channels mentioned below.


## General Guidelines

For general information about contributing to open-source and the Fatiando a Terra
projects, please refer to our 
[standard Contributing Guide](https://github.com/fatiando/community/blob/main/CONTRIBUTING.md).

This document also contains guidelines specific to this repository below.


## Ground Rules

The goal is to maintain a diverse community that's pleasant for everyone.
**Please be considerate and respectful of others**.
Everyone must abide by our 
[Code of Conduct](https://github.com/fatiando/community/blob/main/CODE_OF_CONDUCT.md) 
and we encourage all to read it carefully.


## Requirements for datasets

The following are the requirements that datasets need to meet in oder to be 
considered for this project.

> **Definitions:**
> 
> * *Source dataset*: the original data as distributed by the data owners/creators.
> * *Output dataset*: the modified/repackaged version that we distribute.

Source datasets must:

1. Be either in the public domain or distributed under an open licence that does not
   place restrictions on reuse beyond attribution or using the same license. 
   For example, CC-BY and CC-BY-SA are acceptable but not CC-BY-NC.
1. Represent a common real-world application.
1. Contain interesting features that **lead to teachable moments** for tutorials.
   for example, interesting anomalies easily associated with geology, large gaps in
   bathymetry lead to interesting interpolation issues, etc.

Output datasets should:

1. Contain standard and descriptive variable names. For example, "longitude" 
   instead of "LON", "gravity_disturbance_mgal" instead of "FAA", "easting_m"
   instead of "x". 
1. Include associated metadata (datum, license, source, etc.) if supported
   by the format. For example, netCDF metadata following CF conventions
   through `.attrs` attributes in xarray.
3. Specify units through appropriate metadata (CF conventions in netCDF or
   column names in CSV, like `gravity_disturbance_mgal`). Exceptions are
   longitude and latitude coordinates which are always in decimal degrees.
1. Strive to be under 10 Mb in size, if possible. This keeps downloads fast,
   particularly when building documentation and testing on CI. Use compression 
   when appropriate and only if it doesn't add difficult to install dependencies.
   Larger files may be considered but should not be used in code that runs on 
   CI to avoid long build times and overloading the data servers.
   
   
## Adding a new dataset

First, open an Issue with information about the proposed dataset for discussion.

If the dataset is found to be acceptible by the maintainers, open a pull request
against the `main` branch of this repository with the proposed changes:

1. Create a folder following the naming convention `location_datatype` (all lower
   case and separated by `_`).
1. Inside that folder, create a Jupyter notebook called `prepare.ipynb` with the
   code for downloading (using [Pooch](https://github.com/fatiando/pooch)),
   formatting (cleaning, slicing, datum conversion, etc), and exporting the 
   new dataset. Follow the conventions in the other notebooks.
1. The output dataset should follow the same naming convention as the folder:
   `location_datatype.extension`.
1. The notebook should create a `preview.jpg` image with a plot of the output
   dataset for easy inspection.
1. If the original data can't be automatically downloaded in the notebook and it
   is under 50 Mb, you may include it in the repository. Feel free to use 
   compression to reduce the size of the file(s).
1. Include the information about the new dataset in the `README.md` file.
