
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from eye_tracking import get_issue_areas, get_issue_areas_standalone
from accelerometer_tracking import export_problems, export_problems_standalone

def load_data(path):
    afe_data = pd.read_json(path + '/AFE_000_CONFIDENTIAL.json')
    afe_data = pd.concat([afe_data, pd.read_json(path + '/AFE_001_CONFIDENTIAL.json')])
    afe_data = pd.concat([afe_data, pd.read_json(path + '/AFE_002_CONFIDENTIAL.json')])
    afe_data = pd.concat([afe_data, pd.read_json(path + '/AFE_003_CONFIDENTIAL.json')])

    gps_data = afe_data['gps'].apply(pd.Series)
    gps_data.reset_index(inplace=True)
    return gps_data

def load_data_by_path(path):
    afe_data = pd.read_json(path)

    gps_data = afe_data['gps'].apply(pd.Series)
    gps_data.reset_index(inplace=True)
    return gps_data

def save_data(path):
    afe_data = pd.read_json(path + '/AFE_000_CONFIDENTIAL.json')
    afe_data = pd.concat([afe_data, pd.read_json(path + '/AFE_001_CONFIDENTIAL.json')])
    afe_data = pd.concat([afe_data, pd.read_json(path + '/AFE_002_CONFIDENTIAL.json')])
    afe_data = pd.concat([afe_data, pd.read_json(path + '/AFE_003_CONFIDENTIAL.json')])

    gps_data = afe_data['gps'].apply(pd.Series)
    gps_data.reset_index(inplace=True)
    return gps_data

def draw_map(gps_data, mapname, path, save):
    BBox = (gps_data.longitude.min()-0.03,   gps_data.longitude.max()+0.03,
            gps_data.latitude.min()-0.03, gps_data.latitude.max()+0.03)
    #print(BBox)
    map_img = plt.imread('data/map.png')
    fig, ax = plt.subplots(figsize=(7.2, 8.3))
    #ax.plot(gps_data.longitude.values, gps_data.latitude.values, 'b-')
    staring_issues = get_issue_areas(path=path)
    posture_issues = export_problems(path)
    """
    mask = []
    for i in range(0, len(gps_data.longitude)):
        if i in staring_issues:
            mask.append(True)
        else:
            mask.append(False)
    mask2 = [not elem for elem in mask]

    """
    #ax.plot(gps_data['longitude'][mask].values, gps_data['latitude'][mask].values, color='red', marker='x', linestyle='') 
    ax.plot(gps_data['longitude'].values, gps_data['latitude'].values, color='blue', linewidth=4)

    for s, e in staring_issues:
        ax.plot(gps_data['longitude'][s:e].values, gps_data['latitude'][s:e].values, color='red', linewidth=8)

    for s, e in posture_issues:
        ax.plot(gps_data['longitude'][s:e].values, gps_data['latitude'][s:e].values, color='violet', linewidth=8)

    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    ax.imshow(map_img, zorder=0, extent=BBox, aspect='equal')

    if (save):
        plt.savefig(mapname)
    else:
        plt.show()
"""
def identify_issues(data1, data2, data3, path1, path2, path3):
    issues = np.empty(1)
    for s,e in get_issue_areas(path = path1):
        np.append(issues, (data1['longitude'][s:e].values, data1['latitude'][s:e].values))

    for s,e in export_problems(path1):
        np.append(issues, (data1['longitude'][s:e].values, data1['latitude'][s:e].values))

    for s,e in get_issue_areas(path = path2):
        np.append(issues, (data2['longitude'][s:e].values, data2['latitude'][s:e].values))

    for s,e in export_problems(path2):
        np.append(issues, (data2['longitude'][s:e].values, data2['latitude'][s:e].values))

    for s,e in get_issue_areas(path = path3):
        np.append(issues, (data3['longitude'][s:e].values, data3['latitude'][s:e].values))

    for s,e in export_problems(path3):
        np.append(issues, (data3['longitude'][s:e].values, data3['latitude'][s:e].values))

    np.savetxt('output/issues.out', issues, delimiter=',')
"""
def draw_map_standalone(mapname, afe_path, imu_path, save):
    gps_data = load_data_by_path(afe_path)
    BBox = (gps_data.longitude.min()-0.03,   gps_data.longitude.max()+0.03,
            gps_data.latitude.min()-0.03, gps_data.latitude.max()+0.03)
    #print(BBox)
    map_img = plt.imread('data/map.png')
    fig, ax = plt.subplots(figsize=(7.2, 8.3))
    #ax.plot(gps_data.longitude.values, gps_data.latitude.values, 'b-')
    staring_issues = get_issue_areas_standalone(path=afe_path)
    posture_issues = export_problems_standalone(imu_path)
    """
    mask = []
    for i in range(0, len(gps_data.longitude)):
        if i in staring_issues:
            mask.append(True)
        else:
            mask.append(False)
    mask2 = [not elem for elem in mask]

    """
    #ax.plot(gps_data['longitude'][mask].values, gps_data['latitude'][mask].values, color='red', marker='x', linestyle='') 
    ax.plot(gps_data['longitude'].values, gps_data['latitude'].values, color='blue', linewidth=4)

    for s, e in staring_issues:
        ax.plot(gps_data['longitude'][s:e].values, gps_data['latitude'][s:e].values, color='red', linewidth=8)

    for s, e in posture_issues:
        ax.plot(gps_data['longitude'][s:e].values, gps_data['latitude'][s:e].values, color='violet', linewidth=8)

    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])
    ax.imshow(map_img, zorder=0, extent=BBox, aspect='equal')

    if (save):
        plt.savefig(mapname)
        plt.show()
    else:
        plt.show()

def create_map(path, mapname, save):
    data = load_data(path)
    draw_map(data, mapname, path, save)

def create_hotspots(path1, path2, path3):
    data1 = load_data(path1)
    data2 = load_data(path2)
    data3 = load_data(path3)
    identify_issues(data1, data2, data3, path1, path2, path3)
    
def create_individual():
    create_map('data/driving_1', 'output/1', True)
    create_map('data/driving_2', 'output/2', True)
    create_map('data/driving_3', 'output/3', True)

#create_hotspots('data/driving_1', 'data/driving_2', 'data/driving_3')
#create_individual()