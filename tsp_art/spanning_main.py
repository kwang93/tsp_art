import voronoi_stippler
import tsp_connector
import spanning_tsp
from PIL import Image


def __main__():

    # load images
    folder_path = "images/"
    image_filename = "spam.png"
    image = Image.open(folder_path + image_filename).convert('L')

    color_bool = False   # no color yet

    # create stipples on image and save image
    voronoi_image = voronoi_stippler.main_voronoi(image, stipple_mult=4, convergence=5, color=color_bool)
    voronoi_image.show()
    voronoi_image.save("output_color/" + image_filename + "_voronoi" + ".png", "PNG")

    tsp_image = tsp_connector.connect_points(image)
    tsp_image.show()

    image = spanning_tsp.connect_points(image)
    image.show()


if __name__ == "__main__":

    __main__()
