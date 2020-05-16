from PIL import Image, ImageDraw
from tsp_solver.greedy import solve_tsp
import numpy as np


# get coordinates of all points
def get_points(stippled_image, width, height):

    loaded_image = stippled_image.load()

    points = []
    blank_pixel = 255
    shaded_pixel = None
    for x in range(width):
        for y in range(height):
            if loaded_image[x, y] != blank_pixel:
                if not shaded_pixel:
                    shaded_pixel = loaded_image[x, y]
                points.append((x, y))

    return points


# get the original color at points
def get_original_color(original_image, points):
    colored_points = []
    color_point_dict = {}
    for i in range(len(points)):
        a = (points[i][0], points[i][1])
        colored_points.append(original_image.getpixel(a))
        color_point_dict[a] = original_image.getpixel(a)
    return colored_points, color_point_dict


# use to reset canvas
def clear_image(width, height, put_pixel, background):
    for y in range(height):
        for x in range(width):
            put_pixel((x, y), background)


# add colored points into image
def draw_image(points, color_point_dict, put_pixel, width, height):
    # points = list(points)
    # print(points)
    # for i in range(len(points)):
    #     pt = int(points[i][0]), int(points[i][1])
    #     if pt == (0, 0):
    #         # Skip pixels at origin - they'll break the TSP art
    #         continue
    #     put_pixel(pt, color_point_dict.get(pt))

    points = list(points)
    for x in range(width):
        for y in range(height):
            if (x, y) not in points:
                # (0,0,0) if background is black and (255,255,255) if white
                put_pixel((x, y), (255,255,255))
            else:
                put_pixel((x, y), color_point_dict.get((x, y)))


# add colors for lines
def line_colors(lines, color_point_dict):

    line_colors = []

    for i in range(len(lines)):
        c1 = list(color_point_dict.get(lines[i][0]))
        c2 = list(color_point_dict.get(lines[i][1]))
        # print("lines: ", lines[i], "colors1", c1, "colors2", c2)
        colors = np.array([c1, c2])
        colors = np.average(colors, axis=0)
        line_colors.append(colors)
    line_colors = np.around(np.array(line_colors)).tolist()

    for i in range(len(line_colors)):
        colors = [int(x) for x in line_colors[i]]
        line_colors[i] = colors
    return line_colors


# get path of points to connect for tsp
def get_path(points, colored_pixels):
    lines = []

    # use points to build triangular distance matrix
    distance_matrix = [[0] * len(points) for dot in range(len(points))]
    # iterate over all points and get distances
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            distance = (points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance

    # use tsp to solve
    paths = solve_tsp(distance_matrix)

    # build array of points on tsp path and return
    p0 = points[paths[0]]
    for path in range(1, len(paths)):
        p1 = points[paths[path]]
        lines.append((p0, p1))
        p0 = p1
    colors_of_lines = line_colors(lines, colored_pixels)
    return lines, colors_of_lines


# run tsp and draw points.
def connect_colored_points(image, coordinates, color_point_dict):


    #image.show()
    print("There are", len(coordinates), "stipples to connect")
    # get path
    path, colors_of_lines = get_path(coordinates, color_point_dict)
    # draw lines, free up space and return image
    draw = ImageDraw.Draw(image)
    count = 0
    for pair in path:
        p1 = pair[0]
        p2 = pair[1]
        r = colors_of_lines[count][0]
        g = colors_of_lines[count][1]
        b = colors_of_lines[count][2]
        try:
            draw.line((p1, p2), fill=(r, g, b), width=3)
        except ValueError:
            # (0,0,0) if background is black and (255,255,255) if white
            draw.line((p1, p2), fill=(255,255,255), width=3)
        count += 1
    del draw
    return image


def main(stippled_image, original_image, background):
    # create new canvas and get pixels
    width, height = original_image.size
    colored_stipple = Image.new("P", (width, height))
    put_pixel = colored_stipple.putpixel

    # get points, get colored pixels
    coordinates = get_points(stippled_image, width, height)
    colored_pixels, color_point_dict = get_original_color(original_image, coordinates)

    # draw colored points over

    clear_image(width, height, put_pixel, background)
    draw_image(coordinates, color_point_dict, put_pixel, width, height)

    colored_stipple.show()
    colored_stipple.save("output_color/" + "colored_stipple.png", "PNG")

    colored_tsp = connect_colored_points(colored_stipple, coordinates, color_point_dict)
    return colored_tsp
