# Global gravity, geoid height, and topography grids

This dataset includes global 10 arc-minute resolution grids of
gravity acceleration (gravitational and centrifugal), geoid height, 
and topography/bathymetry.
Gravity and geoid are generated from the [EIGEN-6C4](https://doi.org/10.5880/icgem.2015.1)
spherical harmonic model.
Topography are generated from a spherical harmonic model of
the [ETOPO1](https://doi.org/10.7289/V5C8276M) ice surface model.

Processing and standardization were performed in
[prepare.ipynb](https://nbviewer.org/github/fatiando/rockhound-data/blob/main/gravity-topography-global/prepare.ipynb).

## Data files

| File name | Size | Hashes |
|:----------|:-----|:-------|
| `gravity-earth-10arcmin.nc` | 2.5 Mb | `md5:36bc806111d63e29eee08c38bd1d6cd7` `sha256:8d6c75d0f723678b175a9ddb929aee38b155bb5dbc54052697dd1a2342699af1` | 
| `geoid-earth-10arcmin.nc` | 1.3 Mb | `md5:76117ceca7f31fe17122278370996303` `sha256:9c4d1676c11d1321b53fb14a1df460748880936efb21ebfabc8b548f2551dfbb` |
| `topography-earth-10arcmin.nc` | 2.7 Mb | `md5:c0c8d1fad9f7046c878d65cfc9d1dc8c` `sha256:046846c21426bd6da0fdf63077dd69b8ef11639017bdc9bf1bf4d5fc75c9b093` |

## License

CC-BY

Original source: Calculated from the EIGEN-6C4 model (licensed CC-BY)
