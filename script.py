import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from scipy.interpolate import splprep, splev
import open3d as o3d

def fill_gaps(points):
    filled_points = []
    for i in range(points.shape[1] - 1):
        start = points[:, i]
        end = points[:, i + 1]
        filled_points.append(start)
        while not np.array_equal(start, end):
            if start[0] < end[0]:
                start[0] += 1
            elif start[0] > end[0]:
                start[0] -= 1
            if start[1] < end[1]:
                start[1] += 1
            elif start[1] > end[1]:
                start[1] -= 1
            filled_points.append(start.copy())
    filled_points.append(points[:, -1])
    return np.array(filled_points).T

new_points_int = np.loadtxt("points.txt", delimiter=',').astype(int).T
filled_points = fill_gaps(new_points_int)

# Define the user-specified depth value
depth_value = 1  # You can change this value as needed

# Duplicate the points to replicate depth
# Create the depth points using np.tile
depth_points = np.vstack((
    np.tile(filled_points[0], depth_value),
    np.tile(filled_points[1], depth_value),
    np.repeat(np.arange(depth_value), len(filled_points[0]))
))

threed_points = np.column_stack(depth_points)
# Create a point cloud from the depth points
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(threed_points)
o3d.visualization.draw_geometries([pcd])