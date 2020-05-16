import tsp_spanning as tsp
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)
from PIL import ImageDraw


# get path of points to connect for tsp
def get_path(points):
    # print(points)
    # use tsp to solve, gets distance matrix and creates mst kruskal result
    paths = tsp.point_tsp(np.asarray(points))
    print(paths)
    return paths


# run tsp and draw points.
def connect_points(image):

    loaded_image = image.load()
    width, height = image.size

    points = []
    blank_pixel = 255
    shaded_pixel = None
    for x in range(width):
        for y in range(height):
            if loaded_image[x, y] != blank_pixel:
                if not shaded_pixel:
                    shaded_pixel = loaded_image[x, y]
                points.append((x, y))

    print("There are", len(points), "stipples to connect")
    print(len(points))
    # get path
    path = get_path(points)
    # draw lines, free up space and return image
    draw = ImageDraw.Draw(image)
    for i in range(0, len(path)):
        #print(path[i][0])
        if (i==len(path)-2):
            break
        p1 = path[i][0], path[i][1]
        p2 = path[i+1][0], path[i+1][1]
        #p1, p2 = np.array(p1).tolist(), np.array(p2).tolist()
        draw.line((p1, p2), fill=0, width=1)
    del draw
    image.show()
    return image
