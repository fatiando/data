# Curated collection of open geophysics data for tutorials and documentation

This is a place to format and prepare public **open-licensed** datasets for
use in our tutorials and documentation.

We include the source code that prepares the datasets for redistribution
by filtering, standardizing, converting coordinates, compressing, etc.
The goal is to make loading the data as easy as possible (e.g., a single
call to `pandas.read_csv` or `xarray.load_dataset`).
Whenever possible, the code also downloads the original data (otherwise the
original data are included in this repository).


## Downloading

The easiest way to download and use the datasets is using [Pooch](https://www.fatiando.org/pooch).
For example, the following code downloads, caches (stores a local copy), verifies the
download integrity, and loads into a `pandas.DataFrame` our Alpine GPS dataset
from the `v1.0.0` release:

```python
import pooch
import pandas

file_path = pooch.retrieve(
    url="doi:10.5281/zenodo.5167357/alps-gps-velocity.csv.xz",
    known_hash="md5:195ee3d88783ce01b6190c2af89f2b14",
)
data = pandas.read_csv(file_path)
```

To load other data from other releases, replace the file name, DOI, and MD5 hash in the code 
above.

### The Ensaio package

These datasets are also accessible through [Ensaio](https://www.fatiando.org/ensaio):

```python
import ensaio.v1 as ensaio

file_path = ensaio.fetch_alps_gps()
data = pandas.read_csv(file_path)
```

Ensaio uses Pooch under the hood but provides a simpler interface,
with the DOI, file names, and hashes all stored internally.


## Contributing

See our [Contributing Guidelines](CONTRIBUTING.md) for information on
proposing new datasets and making changes to this repository.


## Versions

The curated datasets are published through Zenodo. 
Each release is assigned a unique DOI (see the table below).
The entire collection can be reached through
https://doi.org/10.5281/zenodo.5167356

Version | Digital Object Identifier (DOI)
--|--
[v1.0.0](https://github.com/fatiando/data/releases/tag/v1.0.0) | [10.5281/zenodo.5167357](https://doi.org/10.5281/zenodo.5167357)

> **NOTE:** This collection uses [semantic version](https://semver.org/)
> (i.e., `MAJOR.MINOR.BUGFIX` format).
> Major releases mean that backwards incompatible changes were made to the data.
> Minor releases add new data without changing existing files.
> Bug fix releases fix errors in a previous release that makes the data unusable.
> Changes to the current data files will always be published as a major release
> unless the file(s) in the previous release was unusable/corrupted.


## Datasets

| File name | Size | Hashes |
|:----------|:-----|:-------|
| `alps-gps-velocity.csv.xz` | 0.005 Mb | `md5:195ee3d88783ce01b6190c2af89f2b14` `sha256:77f2907c2a019366e5f85de5aafcab2d0e90cc2c378171468a7705cab9938584` |
| `britain-magnetic.csv.xz` | 2.7 Mb | `md5:8dbbda02c7e74f63adc461909358f056` `sha256:4e00894c2e0fa5b9c547719c8ac08adb6e788a7074c0dae9fb1b2767cf494b38` |
| `british-columbia-lidar.csv.xz` | 4.4 Mb | `md5:354c725a95036bd8340bc14e043ece5a` `sha256:03c6f1b99374b8c00c424c788cb6956bc00ab477244bb69835d4171312714fe1` |
| `caribbean-bathymetry.csv.xz` | 7.8 Mb | `md5:a7332aa6e69c77d49d7fb54b764caa82` `sha256:9adaa2ead1cd354206235105489b511c4c46833b2e137a3eadc917243d16f09e` |
| `earth-gravity-10arcmin.nc` | 2.5 Mb | `md5:56df20e0e67e28ebe4739a2f0357c4a6` `sha256:d55134501da0d984f318c0f92e1a15a8472176ec7babde5edfdb58855190273e` |
| `earth-geoid-10arcmin.nc` | 1.3 Mb | `md5:39b97344e704eb68fa381df2eb47da0f` `sha256:e98dd544c8b4b8e5f11d1a316684dfbc2612e2860af07b946df46ed9f782a0f6` |
| `earth-topography-10arcmin.nc` | 2.7 Mb | `md5:c43b61322e03669c4313ba3d9a58028d` `sha256:e45628a3f559ec600a4003587a2b575402d22986651ee48806930aa909af4cf6` |
| `southern-africa-gravity.csv.xz` | 0.14 Mb | `md5:1dee324a14e647855366d6eb01a1ef35` `sha256:f5f8e5eb6cd97f104fbb739cf389113cbf28ca8ee003043fab720a0fa7262cac` |
| `osborne-magnetic.csv.xz` | 2.2 Mb | `md5:a9e680c9b746065a7aea6dc82e198af5` `sha256:243b1f1ed784c8b175db41c546a6d77486fa5e8901def766fef43c04d18ee26a` |


### GPS velocities for the Alpine region

This is a compilation of 3D GPS velocities for the Alps.
The horizontal velocities are reference to the Eurasian frame.
All velocity components and even the position have error estimates,
which is very useful and rare to find in a lot of datasets.

* Original source: [Sánchez et al. (2018)](https://doi.org/10.1594/PANGAEA.886889)
* Original license: CC-BY
* More information: [`prepare.ipynb`](https://nbviewer.org/github/fatiando/data/blob/main/alps-gps-velocity/prepare.ipynb)

### Airborne magnetic survey of Britain

This is a digitized version of an airborne magnetic survey of Britain.
Data are sampled where flight lines crossed contours on the archive maps.
Contains only the total field magnetic anomaly, not the magnetic field
intensity measurements or corrections.
Contains British Geological Survey materials © UKRI 2021.

* Original source: [British Geological Survey](https://www.bgs.ac.uk/datasets/gb-aeromagnetic-survey/)
* Original license: Open Government Licence
* More information: [`prepare.ipynb`](https://nbviewer.org/github/fatiando/data/blob/main/britain-magnetic/prepare.ipynb)

### LiDAR point cloud of the Trail Islands in British Columbia, Canada

This is a point cloud sliced to the small
[Trail Islands](https://apps.gov.bc.ca/pub/bcgnws/names/21973.html) North of
Vancouver to reduce the data size.
The islands have some nice looking topography and their isolated nature creates
problems for some interpolation methods.

* Original source: [LidarBC](https://www2.gov.bc.ca/gov/content/data/geographic-data-services/lidarbc)
* Original license: Open Government Licence - British Columbia
* More information: [`prepare.ipynb`](https://nbviewer.org/github/fatiando/data/blob/main/british-columbia-lidar/prepare.ipynb)

### Single-beam bathymetry of the Caribbean

This dataset is a compilation of several single-beam bathymetry surveys
displaying a wide range of tectonic activity, uneven distribution, and
even clear systematic errors in some of the survey lines.
The original data file was compressed with LZMA to save space and make it
possible to upload it to this GitHub repository.

* Original source: [NOAA NCEI](https://ngdc.noaa.gov/mgg/geodas/trackline.html)
* Original license: Public domain
* More information: [`prepare.ipynb`](https://nbviewer.org/github/fatiando/data/blob/main/caribbean-bathymetry/prepare.ipynb)

### Global gravity, geoid height, and topography grids

This dataset includes global 10 arc-minute resolution grids of
gravity acceleration (gravitational and centrifugal) at 10 km geometric height,
geoid height, and topography/bathymetry (referenced to "sea level").

* Original source: [EIGEN-6C4](https://doi.org/10.5880/icgem.2015.1) (gravity
  and geoid) and [ETOPO1](https://doi.org/10.7289/V5C8276M) ice surface
  (topography) generated by the
  [ICGEM calculation service](http://icgem.gfz-potsdam.de/home)
* Original license: CC-BY (EIGEN-6C4) and public domain (ETOPO1)
* More information: [`prepare.ipynb`](https://nbviewer.org/github/fatiando/data/blob/main/global-gravity-topography/prepare.ipynb)

### Ground gravity of Southern Africa

This is a public domain compilation of ground measurements of gravity from
Southern Africa.
The observations are the absolute gravity values in mGal.
The horizontal datum is not specified and heights are referenced to "sea
level", which we will interpret as the geoid (which realization is likely not
relevant since the uncertainty in the height is probably larger than geoid
model differences).

* Original source: [NOAA NCEI](https://www.ngdc.noaa.gov/)
* Original license: Public domain
* More information: [`prepare.ipynb`](https://nbviewer.org/github/fatiando/data/blob/main/southern-africa-gravity/prepare.ipynb)

### Airborne magnetic data of the Osborne Mine and Lightning Creek sill complex, Australia

This is a section of a survey acquired in 1990 by the Queensland Government,
Australia. The data are good quality with approximately 80 m terrain clearance
and 200 m line spacing. The anomalies are very visible and present interesting
processing and modelling challenges, as well as plenty of literature about
their geology.

* Original source: [Geophysical Acquisition & Processing Section 2019. MIM Data from Mt Isa Inlier, QLD (P1029), magnetic line data, AWAGS levelled. Geoscience Australia, Canberra](http://pid.geoscience.gov.au/dataset/ga/142419)
* Original license: CC-BY
* More information: [`prepare.ipynb`](https://nbviewer.org/github/fatiando/data/blob/main/osborne-magnetic/prepare.ipynb)


## License

All Python source code is made available under the BSD 3-clause license. You
can freely use and modify the code, without warranty, so long as you provide
attribution to the authors.

Unless otherwise specified, all data files and figures created by the code are
available under the Creative Commons Attribution 4.0 License (CC-BY).
The licenses for the original source data are specified in this `README.md`
file and the Jupyter notebooks.
