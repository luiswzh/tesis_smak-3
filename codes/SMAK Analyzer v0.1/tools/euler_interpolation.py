import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp

def slerp_euler(t, t_start, t_end, euler_start, euler_end):
    # Convert Euler angles to quaternions
    quat_start = R.from_euler('xyz', euler_start, degrees=False)
    quat_end = R.from_euler('xyz', euler_end, degrees=False)

    # Perform slerp
    interpolated_quat = Slerp([t_start, t_end], R.concatenate([quat_start, quat_end]))

    # Convert the interpolated quaternion back to Euler angles
    return interpolated_quat(t).as_euler('xyz', degrees=False)

if __name__ == "__main__":
    # Example usage
    euler_start = [0.7601, -0.5635, -3.1314]
    euler_end = [0.73958, -0.6019, 3.08450]
    t = 0.5

    interpolated_euler = slerp_euler(0.1, 0, 1, euler_start, euler_end)
    print("Interpolated Euler angles:", interpolated_euler)