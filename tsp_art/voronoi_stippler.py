from scipy import spatial
from PIL import Image
import numpy as np
import os
import random
import itertools
import math


def clear_image(width, height, put_pixel):
    for y in range(height):
        for x in range(width):
            put_pixel((x, y), 255)


def draw_image(points, put_pixel):
    points = list(points)
    for i in range(len(points)):
        pt = int(points[i][0]), int(points[i][1])
        if pt == (0, 0):
            # Skip pixels at origin - they'll break the TSP art
            continue
        put_pixel(pt, 0)


# create weighted voroni diagram based off of densities
def sum_regions(centroids, centroid_sums, densities, step, width, height):

    # create KDTree, used to find k nearest neighbors
    tree = spatial.KDTree(list(zip(centroids[0], centroids[1])))

    x = np.arange(step / 2.0, width, step)
    y = np.arange(step / 2.0, height, step)
    point_matrix = list(itertools.product(x, y))
    nearest_neighbors = tree.query(point_matrix)[1]

    for i in range(len(point_matrix)):
        point = point_matrix[i]
        x = point[0]
        y = point[1]
        r = densities[int(y)][int(x)]
        centroid_index = nearest_neighbors[i]
        centroid_sums[0][centroid_index] += r * x
        centroid_sums[1][centroid_index] += r * y
        centroid_sums[2][centroid_index] += r


# calculate centroids and update weighted voronoi diagram
def compute_centroids(centroids, centroid_sums, width, height):
    centroid_delta = 0
    for i in range(len(centroids[0])):
        # densities are 0 and put centroids elsewhere
        if not centroid_sums[2][i]:
            centroids[0][i] = random.randrange(width)
            centroids[1][i] = random.randrange(height)
        # update data using riemann sums
        else:
            centroid_sums[0][i] /= centroid_sums[2][i]
            centroid_sums[1][i] /= centroid_sums[2][i]

            p1 = (centroid_sums[0][i] - centroids[0][i]) ** 2
            p2 = (centroid_sums[1][i] - centroids[1][i]) ** 2
            centroid_delta += (p1 + p2)

            centroids[0][i] = centroid_sums[0][i]
            centroids[1][i] = centroid_sums[1][i]
    return centroid_delta


# increase size of image to show whitespace better and draw final output_marv
def magnify_and_draw_points(points, width, height, stipple_mult):
    points = list(points)
    # get magnified image size and create blank canvas
    magnified_size = (width * stipple_mult, height * stipple_mult)
    blank_canvas = Image.new("L", magnified_size)
    put_pixel = blank_canvas.putpixel

    # clear canvas, get points and draw image
    clear_image(magnified_size[0], magnified_size[1], put_pixel)
    magnified_points = [tuple(stipple_mult * x for x in point) for point in points]
    draw_image(magnified_points, put_pixel)
    return blank_canvas


# compute the weighted voronoi stippling for an image
def main_voronoi(image):

    # used to add more stipples for more detail
    stipple_mult = 8

    # convergence goal for the stipples, want centroid delta to be below it
    # most times after 50 iterations it seems to slow down a lot
    # Values tried 0.5, 1, 5, 10, 20, 50
    # 0.5 is to high and it takes forever
    convergence = 0.5

    # set up output folder
    folder_base = "output_pika/"
    os.makedirs(folder_base)

    # load in imagage and get data for it
    image_load = image.load()
    put_pixel = image.putpixel
    width, height = image.size
    stipples = int(math.hypot(height, width) * stipple_mult)

    print("Creating", stipples, "stipples with convergence of", str(convergence) + ".")

    # get random centroids for voroni
    c_X = []
    c_Y = []
    for x in range(stipples):
        c_X.append(random.randrange(width))
    for y in range(stipples):
        c_Y.append(random.randrange(height))
    centroids = [c_X, c_Y]

    # get densities of each pixel
    densities = [[0] * width for y in range(height)]
    for y in range(height):
        for x in range(width):
            densities[y][x] = 1 - image_load[x, y] / 255.0

    # set all pixels in image to be 255
    clear_image(width, height, put_pixel)
    # draw image using centroids

    draw_image(zip(centroids[0], centroids[1]), put_pixel)
    # save image to folder
    image.save(folder_base + "iteration_0.png", "PNG")

    # x,y and density
    centroid_sums = [[0] * stipples, [0] * stipples, [0] * stipples]

    # count number of passes
    iteration = 0
    # used when image has stopped converging
    resolution = 1.0
    done = False
    # used to check convergence
    last_centroid_delta = math.inf
    while not done:

        # iterate
        iteration += 1

        # zero sums before iteration starts
        for component in centroid_sums:
            for ele in range(len(component)):
                component[ele] = 0

        # shade regions and sum centroid regions
        sum_regions(centroids, centroid_sums, densities, resolution, width, height)

        # recompute centroids
        centroid_delta = compute_centroids(centroids, centroid_sums, width, height)

        # print change in centroid
        print(str(iteration) + "   centroid delta: " + str(centroid_delta))

        # save what image looks like after current iteration
        clear_image(width, height, put_pixel)
        draw_image(zip(centroids[0], centroids[1]), put_pixel)
        image.save(folder_base + "iteration_" + str(iteration) + ".png", "PNG")

        # increase resolution if little or no change
        # minimum convergence amount
        min_change = 0.5
        if centroid_delta + min_change >= last_centroid_delta:
            resolution *= 2
            convergence = resolution * convergence
            print("Convergence has slowed, updating convergence")
            print("New convergence is " + str(convergence))

        last_centroid_delta = centroid_delta

        if centroid_delta == 0.0:
            resolution *= 2
            convergence = resolution * convergence
            print("Convergence has slowed, updating convergence")
            print("New convergence is " + str(convergence))

        # exit if reached convergence goal
        elif centroid_delta < convergence * resolution:
            done = True

    # Final print statement.
    print("Magnify image and draw points.")
    return magnify_and_draw_points(zip(centroids[0], centroids[1]), width, height, stipple_mult)
