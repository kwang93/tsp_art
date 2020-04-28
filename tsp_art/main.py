import voronoi_stippler
from PIL import Image
import tsp_connector


def __main__():

    folder_path = "images/"
    image_filename = "suprised_pika.png"
    image = Image.open("output/iteration_33.png").convert('L')
    # image.show()
    # image = image.convert('1')  make black and white for difficult images

    # create stipples on image and save image
    # voronoi_image = voronoi_stippler.main_voronoi(image)
    # voronoi_image.show()
    # voronoi_image.save("output/" + image_filename + "_voronoi" + ".png", "PNG")

    # connect stipples and save image
    print("Connecting stipples")
    tsp_image = tsp_connector.connect_points(image)
    tsp_image.show()
    tsp_image.save("output/" + "a" + "_tsp.png", "PNG")


if __name__ == "__main__":

    __main__()
