import time

import click
import cv2
from PIL import Image

from .processors import generate_cubemap, ConvertProjectionProcessor
from .projections import PROJECTION_CLASSES, PROJECTION_CUBEMAP


@click.command()
@click.option('--in-projection', type=str)
@click.option('--out-projection', type=str)
@click.option('--output', type=click.Path(), default='output.jpg')
@click.option('--output-width', type=int, default=4096)
@click.argument('in_images', nargs=-1, type=click.Path(exists=True))
def main(in_projection, out_projection, output, output_width, in_images):
    click.echo(click.style("input images: #{}".format(len(in_images)), fg='blue'))
    click.echo(click.style("input proj: {}".format(in_projection), fg='blue'))
    click.echo(click.style("output proj: {}".format(out_projection), fg='blue'))

    input_image_path = None
    input_image = None
    if in_projection == PROJECTION_CUBEMAP:
        # validate input images
        if len(in_images) != 6:
            click.echo(click.style("You need to supply 6 images for the cubemap projection", fg='red'))
            return

        # merge the 6 faces into one map
        click.echo("--> Merging cubemap images...")
        merged_image = generate_cubemap(in_images)
        click.echo("    done")

        # TODO use a tmp file instead
        merged_image.save('cubemap.jpg')

        input_image_path = 'cubemap.jpg'
        input_image = merged_image
    else:
        raise ValueError("input projection '{}' not fully implemented yet".format(in_projection))

    if in_projection not in PROJECTION_CLASSES:
        click.echo(click.style("Unknown input projection '{}'".format(in_projection), fg='red'))
        return
    in_proj = PROJECTION_CLASSES[in_projection](input_image.size[0])

    if out_projection not in PROJECTION_CLASSES:
        click.echo(click.style("Unknown output projection '{}'".format(out_projection), fg='red'))
        return
    out_proj = PROJECTION_CLASSES[out_projection](output_width)

    click.echo("--> Converting projections...")
    processor = ConvertProjectionProcessor(input_image_path)
    out = processor.run(in_proj, out_proj)
    click.echo("    done")
        
    cv2.imwrite(output, out)
    click.echo(click.style("Done! Conversion saved at '{}'".format(output), fg='green'))


if __name__ == "__main__":
    main()
