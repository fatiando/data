# Open-access sample data for the Fatiando a Terra project

This is a place to format and prepare public open-licensed datasets for
[RockHound](https://github.com/fatiando/rockhound).

All source datasets should either be public domain or under a permissive
licence (e.g. CC-BY but not CC-BY-NC).

The code in this repository processes the original files into formats easily
loaded by pandas and xarray.
Ideally, the output data files should:

1. Represent a common real-world application and contain interesting features
   that lead to teachable moments for tutorials (e.g., interesting anomalies
   easily associated with geology, large gaps in bathymetry lead to interesting
   interpolation issues, etc).
1. Contain standard and descriptive variable names ("longitude" instead of
   "LON", "gravity_disturbance_mgal" instead of "FAA")
1. Include associated metadata (datum, license, source, units, etc.) if
   supported by the format (netCDF for example, but not CSV).
1. Specify units through appropriate metadata (CF conventions in netCDF or
   column names in CSV, like `gravity_disturbance_mgal`). Exceptions are
   longitude and latitude coordinates which are always in decimal degrees.
1. Be under 10 Mb in size, if possible. This is to keep downloads quick,
   particularly when building documentation on CI. Use compression when
   appropriate and only if it doesn't add extra and hard to install
   dependencies.

## License

See individual files or the notebooks that process them for the respective
licenses. Unless otherwise noted, our output data are licensed CC-BY.
