
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from eye_tracking import get_issue_areas, get_issue_areas_standalone
from accelerometer_tracking import export_problems, export_problems_standalone

# loads data in pre defined from from directory specified in path
def load_data(path):
    afe_data = pd.read_json(path + '/AFE_000_CONFIDENTIAL.json')
    afe_data = pd.concat([afe_data, pd.read_json(path + '/AFE_001_CONFIDENTIAL.json')])
    afe_data = pd.concat([afe_data, pd.read_json(path + '/AFE_002_CONFIDENTIAL.json')])
    afe_data = pd.concat([afe_data, pd.read_json(path + '/AFE_003_CONFIDENTIAL.json')])

    gps_data = afe_data['gps'].apply(pd.Series)
    gps_data.reset_index(inplace=True)
    return gps_data

# loads single datafile specified by path
def load_data_by_path(path):
    afe_data = pd.read_json(path)

    gps_data = afe_data['gps'].apply(pd.Series)
    gps_data.reset_index(inplace=True)
    return gps_data

# draws the route on a map and highlights the problem areas
def draw_map(gps_data, mapname, path, save):
    BBox = (gps_data.longitude.min()-0.03,   gps_data.longitude.max()+0.03,
            gps_data.latitude.min()-0.03, gps_data.latitude.max()+0.03)

    map_img = plt.imread('data/map.png')
    fig, ax = plt.subplots(figsize=(7.2, 8.3))

    staring_issues = get_issue_areas(path=path)
    posture_issues = export_problems(path)


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

# same as draw_map but takes path to data instead of already processed data
def draw_map_standalone(mapname, afe_path, imu_path, save):
    gps_data = load_data_by_path(afe_path)
    BBox = (gps_data.longitude.min()-0.03,   gps_data.longitude.max()+0.03,
            gps_data.latitude.min()-0.03, gps_data.latitude.max()+0.03)

    map_img = plt.imread('data/map.png')
    fig, ax = plt.subplots(figsize=(7.2, 8.3))

    staring_issues = get_issue_areas_standalone(path=afe_path)
    posture_issues = export_problems_standalone(imu_path)

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

# load data from path and draws it on a map
def create_map(path, mapname, save):
    data = load_data(path)
    draw_map(data, mapname, path, save)

# create map for 3 different recording sessions    
def create_individual():
    create_map('data/driving_1', 'output/1', True)
    create_map('data/driving_2', 'output/2', True)
    create_map('data/driving_3', 'output/3', True)

#create_individual()