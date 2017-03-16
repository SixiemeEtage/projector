import cv2
import numpy as np
from PIL import Image

import libprojector


def generate_cubemap(images):
    """
     Compose a cubemap associated with the following cubemap layout

      -------- -------- -------- -------- -------- --------
     |   +x   |   -x   |   +y   |   -y   |   +z   |   -z   |
     |  side  |  side  |  side  |  side  |  side  |  side  |
      -------- -------- -------- -------- -------- --------

    """
    merged_image = None
    side_size = 0
    x_offset, y_offset = (0, 0)
    for idx, img_path in enumerate(images):
        img = Image.open(img_path)
        if merged_image is None:
            side_size = img.size[0]
            cubemap_size = (side_size*6, side_size*1)
            merged_image = Image.new(img.mode, cubemap_size)

        if idx == 0:
            # front side (+x)
            x_offset, y_offset = (0*side_size, 0*side_size)
        elif idx == 1:
            # back side (-x)
            x_offset, y_offset = (1*side_size, 0*side_size)
        elif idx == 2:
            # left side (+y)
            x_offset, y_offset = (2*side_size, 0*side_size)
        elif idx == 3:
            # right side (-y)
            x_offset, y_offset = (3*side_size, 0*side_size)
        elif idx == 4:
            # top side (+z)
            x_offset, y_offset = (4*side_size, 0*side_size)
        elif idx == 5:
            # bottom side (-z)
            x_offset, y_offset = (5*side_size, 0*side_size)
        else:
            raise ValueError("Unknown side index")

        merged_image.paste(img, (x_offset, y_offset))

    return merged_image


def split_cubemap(map_image):
    """
     Cubemap splitting associated with the following cubemap layout

      -------- -------- -------- -------- -------- --------
     |   +x   |   -x   |   +y   |   -y   |   +z   |   -z   |
     |  side  |  side  |  side  |  side  |  side  |  side  |
      -------- -------- -------- -------- -------- --------

    """
    assert isinstance(map_image, np.ndarray)
    splitted_images = {}
    if map_image.shape[1] % 6 != 0:
        raise ValueError("The cubemap layout doesn't seem to be valid, it needs to be 6:1")
    side_x_size = int(map_image.shape[1] / 6)
    side_y_size = int(map_image.shape[0])
    if side_x_size != side_y_size:
        raise ValueError("The cubemap doesn't seem to be valid, the face sizes are not equal.")

    faces_offsets = {
        "+x": (0, 0),
        "-x": (1, 0),
        "+y": (2, 0),
        "-y": (3, 0),
        "+z": (4, 0),
        "-z": (5, 0),
    }
    for face in faces_offsets:
        offset_indexes = faces_offsets[face]
        top_x, top_y = (side_x_size * offset_indexes[0], side_y_size * offset_indexes[1])
        bottom_x, bottom_y = top_x + side_x_size, top_y + side_y_size
        img = map_image[top_y:bottom_y, top_x:bottom_x]
        splitted_images[face] = img

    return splitted_images


class ConvertProjectionProcessor(object):

    def __init__(self, input_image_path):
        self.image = cv2.imread(input_image_path)
        image_size = (self.image.shape[1], self.image.shape[0])
        self._setup(image_size)

    def _setup(self, image_size):
        pass

    def run(self, input_proj, output_proj):
        """Generate the preview"""
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
