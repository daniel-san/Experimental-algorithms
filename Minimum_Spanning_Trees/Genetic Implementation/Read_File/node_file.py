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
        file_points.write('%d %d\n' % (point.X, point.Y))

    file_points.close()
