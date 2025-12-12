import time
from pyrplidar import PyRPlidar

MIN_DISTANCE = 50     
MAX_DISTANCE = 300   
MIN_ANGLE = 135
MAX_ANGLE = 225


def count_objects(points, angle_gap=5, distance_gap=50):
    """
    Cluster points into objects.
    Returns:
        num_objects, clusters
        - num_objects: integer
        - clusters: list of clusters, each cluster is a list of (angle, dist)
    """

    if not points:
        return 0, []

    # Sort by angle
    points = sorted(points, key=lambda x: x[0])

    clusters = []
    current_cluster = [points[0]]

    for i in range(1, len(points)):
        angle_diff = abs(points[i][0] - points[i-1][0])
        dist_diff = abs(points[i][1] - points[i-1][1])

        # Start a new object
        if angle_diff > angle_gap or dist_diff > distance_gap:
            clusters.append(current_cluster)
            current_cluster = [points[i]]
        else:
            current_cluster.append(points[i])

    clusters.append(current_cluster)  # last cluster

    return len(clusters), clusters



def lidar5():
    lidar = PyRPlidar()
    lidar.connect(port="/dev/ttyUSB0", baudrate=460800, timeout=3)
    lidar.set_motor_pwm(500)
    time.sleep(2)
    scan_generator = lidar.force_scan()

    try:
        points = []
        prev_angle = None

        for scan in scan_generator():

            # Filter points
            if MIN_DISTANCE <= scan.distance <= MAX_DISTANCE and MIN_ANGLE <= scan.angle <= MAX_ANGLE:
                points.append((int(scan.angle), int(scan.distance)))

            # Detect full rotation
            if prev_angle is not None and scan.angle < prev_angle:
                
                num_objects, clusters = count_objects(points)

                if num_objects == 0:
                    print("\nObjetos no detectados\n")
                else:
                    #print(f"\nObjetos detectados: {num_objects}\n")
                    for idx, cluster in enumerate(clusters):
                        
                        for ang, dist in cluster:
                            
                            print(f"Objeto {idx+1} {ang}°,{dist}mm-----------------")
                        print()

                points.clear()

            prev_angle = scan.angle

    except KeyboardInterrupt:
        print("\nStopped")

    finally:
        lidar.stop()
        lidar.set_motor_pwm(0)
        lidar.disconnect()



if __name__ == "__main__":
    lidar5()
