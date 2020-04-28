from PIL import ImageDraw
from tsp_solver.greedy import solve_tsp


# get path of points to connect for tsp
def get_path(points):
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
    return lines


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
    # get path
    path = get_path(points)
    # draw lines, free up space and return image
    draw = ImageDraw.Draw(image)
    for pair in path:
        p1 = pair[0]
        p2 = pair[1]
        draw.line((p1, p2), fill=shaded_pixel, width=1)
    del draw
    return image
