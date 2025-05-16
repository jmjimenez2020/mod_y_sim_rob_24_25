import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from rclpy.serialization import deserialize_message
import rosbag2_py
from rosidl_runtime_py.utilities import get_message

bag_directory = "/home/chemijg02/Escritorio/mod_y_sim_rob_24_25/rosbag/rosbag2_2025_05_16-11_30_05"

arm_joint_names = [
    "arm_02_link_joint",
    "arm_04_link_joint",
    "arm_06_link_joint",
    "arm_08_link_joint",
    "arm_10_link_joint",
    "arm_11_link_joint"
]

wheel_names = ["left_front_wheel_link_joint", "left_back_wheel_link_joint", 
                "right_front_wheel_link_joint", "right_back_wheel_link_joint"]

reader = rosbag2_py.SequentialReader()
storage_options = rosbag2_py.StorageOptions(uri=bag_directory, storage_id="mcap")
converter_options = rosbag2_py.ConverterOptions("", "")
reader.open(storage_options, converter_options)

joint_states_arm = []
joint_states_wheels = []
imu_data = []

while reader.has_next():
    (topic, data, t) = reader.read_next()

    if topic == '/joint_states':
        joint_state_msg = deserialize_message(data, get_message('sensor_msgs/msg/JointState'))
        
        filtered_efforts_arm = []
        for an in arm_joint_names:
            if an in joint_state_msg.name:
                i = joint_state_msg.name.index(an)
                filtered_efforts_arm.append(abs(joint_state_msg.effort[i]))
            else:
                filtered_efforts_arm.append(0.0)
        joint_states_arm.append((t / 1e9, filtered_efforts_arm))

        filtered_positions_wheels = []
        for wn in wheel_names:
            if wn in joint_state_msg.name:
                i = joint_state_msg.name.index(wn)
                filtered_positions_wheels.append(joint_state_msg.position[i])
            else:
                filtered_positions_wheels.append(np.nan)
        joint_states_wheels.append((t / 1e9, filtered_positions_wheels))

    elif topic == '/imu/data':
        imu_msg = deserialize_message(data, get_message('sensor_msgs/msg/Imu'))
        acc = imu_msg.linear_acceleration
        imu_data.append((t / 1e9, acc.x, acc.y, acc.z))

# ARM JOINTS
df_arm = pd.DataFrame(joint_states_arm, columns=['timestamp', 'efforts'])
efforts_arm = pd.DataFrame(df_arm['efforts'].tolist(), columns=arm_joint_names)
df_arm = pd.concat([df_arm['timestamp'], efforts_arm], axis=1)
df_arm['timestamp'] = df_arm['timestamp'] - df_arm['timestamp'].iloc[0]

plt.figure(figsize=(12, 8))
for joint in arm_joint_names:
    plt.plot(df_arm['timestamp'], df_arm[joint], label=f'{joint}')
plt.xlabel('Tiempo (s)')
plt.ylabel('G-parcial (Fuerza)')
plt.title('tiempo vs G-parcial')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# WHEELS
df_wheels = pd.DataFrame(joint_states_wheels, columns=['timestamp', 'positions'])
positions_wheels = pd.DataFrame(df_wheels['positions'].tolist(), columns=wheel_names)
df_wheels = pd.concat([df_wheels['timestamp'], positions_wheels], axis=1)
df_wheels['timestamp'] = df_wheels['timestamp'] - df_wheels['timestamp'].iloc[0]

plt.figure(figsize=(12, 8))
for wheel in wheel_names:
    plt.plot(df_wheels['timestamp'], df_wheels[wheel], label=f'{wheel}')
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición')
plt.title('tiempo vs posición de cada una de las ruedas')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# IMU
df_imu = pd.DataFrame(imu_data, columns=['timestamp', 'acc_x', 'acc_y', 'acc_z'])
df_imu['timestamp'] = df_imu['timestamp'] - df_imu['timestamp'].iloc[0]

plt.figure(figsize=(12, 8))
plt.plot(df_imu['timestamp'], df_imu['acc_x'], label='Acc X')
plt.plot(df_imu['timestamp'], df_imu['acc_y'], label='Acc Y')
plt.plot(df_imu['timestamp'], df_imu['acc_z'], label='Acc Z')
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleración (m/s²)')
plt.title('tiempo vs aceleración de las ruedas')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

