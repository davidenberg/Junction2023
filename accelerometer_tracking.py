import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from eye_tracking import group_continuous_integers

def track_sleep(data):
    timer = 0
    problem_areas = []
    for i in data.index:
        if (abs(data['pitch'][i]) > 20 or abs(data['roll'][i]) > 20):
            timer += 1
            if timer > 150:
                problem_areas.append(i)
        else:
            timer = 0
    return problem_areas

def load_data():
    imu_data = pd.read_json('data/driving_1/IMU_000_CONFIDENTIAL.json')
    imu_data = pd.concat([imu_data, pd.read_json('data/driving_1/IMU_001_CONFIDENTIAL.json')])
    imu_data = pd.concat([imu_data, pd.read_json('data/driving_1/IMU_002_CONFIDENTIAL.json')])
    imu_data = pd.concat([imu_data, pd.read_json('data/driving_1/IMU_003_CONFIDENTIAL.json')])

    imu_data[['x', 'y', 'z','','','','']] =imu_data.v.tolist()
    imu_data[['time', '', '','']] =imu_data.i.tolist()
    imu_data['time_s'] = (imu_data['time'].values - imu_data['time'].iloc[0])* 10**-3
    imu_data['y'] = imu_data['y']
    imu_data.reset_index(inplace=True)

    return imu_data

def calculate_angles(data):
    processed_data = pd.DataFrame()
    processed_data['time'] = data['time_s']

    processed_data['pitch'] = np.arctan2(-data['z'], data['y']) * 180/math.pi
    processed_data['roll'] = np.arctan2(-data['x'], data['y']) * 180/math.pi

    return processed_data

def plot(data, problem_areas):
    plt.plot(data['time'].values, data['pitch'].values, label='Pitch')
    plt.plot(data['time'].values, data['roll'].values, label='Roll')
    for i in problem_areas:
        s, e = i
        plt.axvspan(data['time'][s], data['time'][e], color = 'red', alpha=0.5, lw=1)

    plt.legend()
    plt.ylabel('Angle')
    plt.xlabel('Time (s)')
    plt.show()

data = load_data()
angle_data = calculate_angles(data)
problems = track_sleep(angle_data) 
problems = group_continuous_integers(problems)
plot(angle_data, problems)

