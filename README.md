# projector

[![build-status-image]][travis]

> Compliments and criticism are all ultimately based on some form of projection.
> *Billy Corgan*

## Installation

### Install Requirements

```sh
$ brew install opencv3 --with-python
$ brew install boost --with-python
$ brew install boost-python
$ brew link --force opencv3
```

### Install the C++ native lib

```sh
$ git clone https://github.com/SixiemeEtage/projector
$ cd projector
$ mkdir -p native/build && cd native/build
$ cmake .. \
    -DPYTHON_DESIRED_VERSION=2.X \
    -DPYTHON2_EXECUTABLE=$(which python) \
    -DPYTHON2_LIBRARY=$(python2-config --prefix)/lib/libpython2.7.dylib \
    -DPYTHON2_INCLUDE_DIR=$(python2-config --prefix)/include/python2.7/ \
    -DPYTHON2_NUMPY_INCLUDE_DIRS=/usr/local/Cellar/numpy/1.12.0/lib/python2.7/site-packages/numpy/core/include/ \
    -DBOOST_ROOT=/usr/local/Cellar/boost@1.60/1.60.0 \
    -DBoost_INCLUDE_DIR=/usr/local/Cellar/boost@1.60/1.60.0/include
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
