import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

def load_data_by_path(path):
    imu_data = pd.read_json(path + '/IMU_000_CONFIDENTIAL.json')
    imu_data = pd.concat([imu_data, pd.read_json(path + '/IMU_001_CONFIDENTIAL.json')])
    imu_data = pd.concat([imu_data, pd.read_json(path + '/IMU_002_CONFIDENTIAL.json')])
    imu_data = pd.concat([imu_data, pd.read_json(path + '/IMU_003_CONFIDENTIAL.json')])

    imu_data[['x', 'y', 'z','','','','']] =imu_data.v.tolist()
    imu_data[['time', '', '','']] =imu_data.i.tolist()
    imu_data['time_s'] = (imu_data['time'].values - imu_data['time'].iloc[0])* 10**-3
    imu_data['y'] = imu_data['y']
    imu_data.reset_index(inplace=True)

    return imu_data

def load_single_datafile_by_path(path):
    imu_data = pd.read_json(path)

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
    fig = plt.figure(figsize=(10, 5))

    plt.plot(data['time'].values, data['pitch'].values, label='Pitch')
    plt.plot(data['time'].values, data['roll'].values, label='Roll')
    for i in problem_areas:
        s, e = i
        plt.axvspan(data['time'][s], data['time'][e], color = 'red', alpha=0.5, lw=1)

    plt.legend()
    plt.ylabel('Angle')
    plt.xlabel('Time (s)')
    
    def animate(i):

        plt.clf()
        if (i + 1000 < data['time'].size):
            plt.plot(data['time'].values[i:i+1000], data['pitch'].values[i:i+1000], label='Pitch')
            plt.plot(data['time'].values[i:i+1000], data['roll'].values[i:i+1000], label='Roll')

            for s, e in problem_areas:
                if data['time'][s] < data['time'][i+1000] and data['time'][s] > data['time'][i] :
                    plt.axvspan(data['time'][s], min(data['time'][e], data['time'][i + 1000]), color = 'red', alpha=0.5, lw=1)
        else:
            plt.plot(data['time'].values[i:], data['pitch'].values[i:], label='Pitch')
            plt.plot(data['time'].values[i:], data['roll'].values[i:], label='Roll')

            for s, e in problem_areas:
                if data['time'][s] < data['time'].iloc[-1] and data['time'][s] > data['time'][i] :
                    plt.axvspan(data['time'][s], min(data['time'][e], data['time'].iloc[-1]), color = 'red', alpha=0.5, lw=1)

        # Add a legend
        plt.legend()
    ani = animation.FuncAnimation(fig, animate, frames=data['time'][1000:3000:10].index, repeat=True, interval=1)
    plt.show()
    #ani.save('animations/accelerometer.gif', writer='pillow')

def analysis():
    data = load_data()
    angle_data = calculate_angles(data)
    problems = track_sleep(angle_data) 
    problems = group_continuous_integers(problems)
    plot(angle_data, problems)

def analysis_by_path(path):
    data = load_data_by_path(path)
    angle_data = calculate_angles(data)
    problems = track_sleep(angle_data) 
    problems = group_continuous_integers(problems)
    plot(angle_data, problems)

def acc_analysis(path):
    data = load_single_datafile_by_path(path)
    angle_data = calculate_angles(data)
    problems = track_sleep(angle_data)
    problems = group_continuous_integers(problems)
    plot(angle_data, problems)

def export_problems(path):
    data = load_data_by_path(path)
    angle_data = calculate_angles(data)
    problems = track_sleep(angle_data) 
    return group_continuous_integers(problems)

def export_problems_standalone(path):
    data = load_single_datafile_by_path(path)
    angle_data = calculate_angles(data)
    problems = track_sleep(angle_data) 
    return group_continuous_integers(problems)

#analysis()
#analysis_by_path('data/driving_1')

