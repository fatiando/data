# Curated collection of open geophysics data for tutorials and documentation

This is a place to format and prepare public open-licensed datasets for
use in our tutorials and documentation. 
We include the source code that prepares the datasets for redistribution
by filtering, standardizing, converting coordinates, compressing, etc.
The goals is to make loading the data as easy as possible (e.g., a single
call to `pandas.read_csv` or `xarray.load_dataset`).
When possible, the code also downloads the original data (otherwise the
original data are included in this repository).

The curated datasets will be published in a Zenodo or figshare archive
and downloaded with Pooch in tutorial notebooks and source code.

## Requirements for included datasets

All source datasets must:

1. Be either in the public domain or distributed under a permissive licence 
   (e.g. CC-BY but not CC-BY-NC).    
1. Represent a common real-world application.
1. Contain interesting features that lead to teachable moments for tutorials 
   (e.g., interesting anomalies easily associated with geology, large gaps in 
   bathymetry lead to interesting interpolation issues, etc).

The curated output data should:

1. Contain standard and descriptive variable names ("longitude" instead of
   "LON", "gravity_disturbance_mgal" instead of "FAA")
1. Include associated metadata (datum, license, source, etc.) if supported 
   by the format (e.g. netCDF following CF conventions, but not CSV).
3. Specify units through appropriate metadata (CF conventions in netCDF or
   column names in CSV, like `gravity_disturbance_mgal`). Exceptions are
   longitude and latitude coordinates which are always in decimal degrees.
1. Be under 10 Mb in size, if possible. This is to keep downloads quick,
   particularly when building documentation on CI. Use compression when
   appropriate and only if it doesn't add extra and difficult to install
   dependencies.

## License

See individual data files or the notebooks that process them for the respective
licenses. Unless otherwise noted, our output data are licensed CC-BY.

All source code is available under the BSD 3-clause license.
