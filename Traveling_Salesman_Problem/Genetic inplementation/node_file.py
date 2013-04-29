def load(file_name):
    points = []

    file_points = open(file_name, 'r')

    for line in file_points.readlines():
        string_point = line.split()
        point = int(string_point[0]), int(string_point[1])
        points.append(point)

    file_points.close()

    return points

def save(file_name, points):
    file_points = open(file_name, 'w')

    for point in points:
        x, y = point
        file_points.write('%f %f\n' % (x, y))

    file_points.close()
