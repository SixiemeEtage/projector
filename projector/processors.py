import cv2
import numpy as np
from PIL import Image

import libprojector


def generate_cubemap(images):
    merged_image = None
    side_size = 0
    x_offset, y_offset = (0, 0)
    for idx, img_path in enumerate(images):
        img = Image.open(img_path)
        if merged_image is None:
            side_size = img.size[0]
            cubemap_size = (side_size*4, side_size*3)
            merged_image = Image.new(img.mode, cubemap_size)

        if idx == 0:
            # front side (+x)
            x_offset, y_offset = (1*side_size, 1*side_size)
        elif idx == 1:
            # back side (-x)
            x_offset, y_offset = (3*side_size, 1*side_size)
        elif idx == 2:
            # left side (+y)
            x_offset, y_offset = (2*side_size, 1*side_size)
        elif idx == 3:
            # right side (-y)
            x_offset, y_offset = (0*side_size, 1*side_size)
        elif idx == 4:
            # top side (+z)
            x_offset, y_offset = (0, 0)
        elif idx == 5:
            # bottom side (-z)
            x_offset, y_offset = (0, 2*side_size)
        else:
            raise ValueError("Unknown side index")

        merged_image.paste(img, (x_offset, y_offset))

    return merged_image


class ConvertProjectionProcessor(object):

    def __init__(self, input_image_path):
        self.image = cv2.imread(input_image_path)
        image_size = (self.image.shape[1], self.image.shape[0])
        self._setup(image_size)

    def _setup(self, image_size):
        pass

    def run(self, input_proj, output_proj):
        """Generate the preview"""
        # first we resize the input image
        # so that the remaping step produce a nice image
        # TODO implement this optimization
        # optimal_size = self._input_optimal_size()
        # if optimal_size != self.image_size:
        #     resized_image = cv2.resize(self.image, optimal_size)
        # else:
        #     resized_image = self.image
        resized_image = self.image

        # build the remaping maps
        P = libprojector.ProjectionConvertor(
            input_proj.get_projection(),
            output_proj.get_projection()
        )
        P.convert()
        map_x = P.get_map_x()
        map_y = P.get_map_y()

        out = cv2.remap(resized_image, map_x, map_y, cv2.INTER_LANCZOS4, None, cv2.BORDER_WRAP)
        return out
