import libprojector

PROJECTION_EQUIRECTANGULAR = 'equirectangular'
PROJECTION_CUBEMAP = 'cubemap'


class BaseProj(object):
    
    def __init__(self, image_width, options):
        self.image_width = image_width
        self.options = options

    def get_projection(self):
        raise NotImplementedError


class EquirectangularProj(BaseProj):
    
    def get_projection(self):
        width = self.image_width
        height = self.image_width / 2
        return libprojector.SphericalProjection(width, height)


class CubemapProj(BaseProj):
    
    def get_projection(self):
        side_width = int(self.image_width / 4)
        border_padding = self.options.get('border_padding', 0)
        return libprojector.CubemapProjection(side_width, border_padding)


PROJECTION_CLASSES = dict((
    (PROJECTION_EQUIRECTANGULAR, EquirectangularProj),
    (PROJECTION_CUBEMAP, CubemapProj),
))
