import numpy as np
from numpy import average
import time
from pyrplidar import PyRPlidar
from gpiozero import Buzzer
import RPi.GPIO as gpio

MIN_DISTANCE = 50     
MAX_DISTANCE = 300   
MIN_ANGLE = 135
MAX_ANGLE = 225

pb=2
gpio.setmode(gpio.BCM)

gpio.setup(pb,gpio.OUT)

gpio.output(pb,gpio.LOW)



def get_n_column(matrix, n):
  
    if matrix!=0:
        return [row[n] for row in matrix]
    else:
        return []
        
def averageXD(matrix):
  column1=np.array(get_n_column(matrix, 0))
  column2=np.array(get_n_column(matrix, 1))
  column3=np.array(get_n_column(matrix, 2))
  y=1
  n=0
  avr1=[]
  avr2=[]


    
  while n!=len(column1):
      avr1.append(round(np.average(column2[n:n+count_occurrences(column1, y)]),2))
      avr2.append(round(np.average(column3[n:n+count_occurrences(column1, y)]),2))
      n+=count_occurrences(column1, y)
      y+=1
    
  return avr1,avr2

def count_occurrences(vector, x):
  count = 0
  for element in vector:
    if element == x:
      count += 1
  return count

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
    n=0
    gpio.SETMODE(pb,HIGH)
    try:
        points = []
        prev_angle = None
        output=[]
        

        for scan in scan_generator():
            #gpio.output(pb,LOW)

            # Filter points
            if MIN_DISTANCE <= scan.distance <= MAX_DISTANCE and MIN_ANGLE <= scan.angle <= MAX_ANGLE:
                #gpio.OUTPUT(pb,HIGH)
                points.append((int(scan.angle-180), int(scan.distance)))

            # Detect full rotation
            t=0
            if prev_angle is not None and scan.angle < prev_angle:
                
                num_objects, clusters = count_objects(points)

                if num_objects == 0:
                    output=False
                else:
                    #print(f"\nObjetos detectados: {num_objects}\n")
                    for idx, cluster in enumerate(clusters):
                        
                        for ang, dist in cluster:
                             output.append([idx+1,ang,dist]) 
                        #print()

                points.clear()
                averageXD(output)
                if n>=10:
                    print(averageXD(output))
                    
                    n=0
                else:
                    n+=1
                
                output=[]

            prev_angle = scan.angle

    except KeyboardInterrupt:
        print("\nStopped")

    finally:
        lidar.stop()
        lidar.set_motor_pwm(0)
        lidar.disconnect()



if __name__ == "__main__":
    lidar5()







