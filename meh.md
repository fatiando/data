These datasets are co-located global grids of absolute gravity (gravitational +
centrifugal component), ETOPO1 "ice-surface" topography, and geoid height at 10
arc-minute resolution. This notebook loads the grids from their text files,
sets proper CF-compliant metadata, and saves them to compressed netCDF for a
smaller file size (requires the netcdf4 library for loading). Coordinates and
geoid heights are referenced to WGS84 while topography is defined as "height
above mean sea level" (which we will consider to be the geoid).

License: CC-BY (EIGEN-6C4) and public domain (ETOPO1)
Original source: Calculated from the EIGEN-6C4 model (licensed CC-BY) using the
ICGEM calculation service
