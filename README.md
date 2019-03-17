# projector

[![build-status-image]][travis]

> Compliments and criticism are all ultimately based on some form of projection.
> *Billy Corgan*

## Installation

### Install Requirements

```sh
$ brew install cmake
$ brew install opencv4
$ brew install boost-python
```

### Install the C++ native lib

```sh
$ git clone https://github.com/SixiemeEtage/projector
$ cd projector
$ mkdir -p native/build && cd native/build
$ cmake .. \
    -DPYTHON_DESIRED_VERSION=3.X \
    -DPYTHON3_EXECUTABLE=$(which python) \
    -DPYTHON3_LIBRARY=$(python3-config --prefix)/lib/libpython3.7.dylib \
    -DPYTHON3_INCLUDE_DIR=$(python3-config --prefix)/include/python3.7m/ \
    -DPYTHON3_NUMPY_INCLUDE_DIRS=$(python3-config --prefix)/lib/python3.7/site-packages/numpy/core/include/ \
    -DBOOST_ROOT=$(brew --prefix)/Cellar/boost/1.68.0_1 \
    -DBoost_INCLUDE_DIR=/usr/local/Cellar/boost/1.68.0_1/include
$ make
$ make install
```

### Install the python binding

```sh
$ pip install .
```

## Usage

```sh
$ projector --in-projection=cubemap --out-projection=equirectangular ./examples/cubemap_high_res/cubemap_+x.jpg ./examples/cubemap_high_res/cubemap_-x.jpg ./examples/cubemap_high_res/cubemap_+y.jpg ./examples/cubemap_high_res/cubemap_-y.jpg ./examples/cubemap_high_res/cubemap_+z.jpg ./examples/cubemap_high_res/cubemap_-z.jpg
```

## Credits

Tools used in rendering this package:

*  [`Cookiecutter`][Cookiecutter]
*  [`cookiecutter-pypackage`][cookiecutter-pypackage]

## Contact

[Pierre Dulac][github-dulaccc]  
[@dulaccc][twitter-dulaccc]

## License

`projector` is available under the MIT license. See the [LICENSE](LICENSE) file for more info.


[build-status-image]: https://img.shields.io/travis/SixiemeEtage/projector.svg
[travis]: https://travis-ci.org/SixiemeEtage/projector

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
[github-dulaccc]: https://github.com/dulaccc
[twitter-dulaccc]: https://twitter.com/dulaccc
