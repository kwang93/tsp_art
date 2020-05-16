import voronoi_stippler
import tsp_connector
import get_color
from PIL import Image


def __main__():

    # load images
    folder_path = "images/"
    image_filename = "marv.jpg"
    image = Image.open(folder_path + image_filename).convert('L')

    original_image = Image.open(folder_path + image_filename)
    # converts to remove if more than 255 colors, some photos have more than 255 which
    # causes program to crash comment out if not needed
    original_image = original_image.convert('P')
    original_image = original_image.convert('RGB')
    original_image.show()
    color_bool = True

    # create stipples on image and save image
    voronoi_image = voronoi_stippler.main_voronoi(image, stipple_mult=6, convergence=30, color=color_bool)
    voronoi_image.show()
    voronoi_image.save("output_color/" + image_filename + "_voronoi" + ".png", "PNG")

    # colored tsp
    # (255,255,255) for black background and (0,0,0) for white
    if color_bool:
        print("Coloring tsp")
        colored_image = get_color.main(Image.open(voronoi_image), original_image, background=(0,0,0))
        colored_image.show()
        colored_image.save("marv" + "_tsp.png", "PNG")
    else:
        # connect stipples and save image
        print("Connecting stipples")
        # tsp_image = tsp_connector.connect_points(voronoi_image)
        # tsp_image.show()
        # tsp_image.save("output/" + "name" + "_tsp.png", "PNG")


if __name__ == "__main__":

    __main__()
