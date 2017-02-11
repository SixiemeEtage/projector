# Cheet sheet

## Compile and test

For simplicity, this command can be helpful for testing new projections or debugging

```sh
$ make install && \
  cp /usr/local/lib/python2.7/site-packages/libprojector.so /usr/local/data/virtualenvs/projector/lib/python2.7/site-packages && \
  projector --in-projection cubemap --cubemap-border-padding 1 --out-projection equirectangular examples/cubemap2equirectangular/cubemap_+x.jpg examples/cubemap2equirectangular/cubemap_-x.jpg examples/cubemap2equirectangular/cubemap_+y.jpg examples/cubemap2equirectangular/cubemap_-y.jpg examples/cubemap2equirectangular/cubemap_+z.jpg examples/cubemap2equirectangular/cubemap_-z.jpg
```
