
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def scale_to_img(points, lat_lon, h_w):
    """
    Conversion from latitude and longitude to the image pixels.
    It is used for drawing the GPS records on the map image.
    :param lat_lon: GPS record to draw (lat1, lon1).
    :param h_w: Size of the map image (w, h).
    :return: Tuple containing x and y coordinates to draw on map image.
    """
    # https://gamedev.stackexchange.com/questions/33441/how-to-convert-a-number-from-one-min-max-set-to-another-min-max-set/33445
    old = (points[2], points[0])
    new = (0, h_w[1])
    y = ((lat_lon[0] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
    old = (points[1], points[3])
    new = (0, h_w[0])
    x = ((lat_lon[1] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
    # y must be reversed because the orientation of the image in the matplotlib.
    # image - (0, 0) in upper left corner; coordinate system - (0, 0) in lower left corner
    return int(x), h_w[1] - int(y)

def load_data():
    afe_data = pd.read_json('data/driving_1/AFE_000_CONFIDENTIAL.json')
    afe_data = pd.concat([afe_data, pd.read_json('data/driving_1/AFE_001_CONFIDENTIAL.json')])
    afe_data = pd.concat([afe_data, pd.read_json('data/driving_1/AFE_002_CONFIDENTIAL.json')])
    afe_data = pd.concat([afe_data, pd.read_json('data/driving_1/AFE_003_CONFIDENTIAL.json')])

    gps_data = afe_data['gps'].apply(pd.Series)
    gps_data.reset_index(inplace=True)
    return gps_data

def draw_map(gps_data):
    BBox = (gps_data.longitude.min()-0.03,   gps_data.longitude.max()+0.03,
            gps_data.latitude.min()-0.03, gps_data.latitude.max()+0.03)
    print(BBox)
    image = Image.open('data/map.png', 'r')  # Load map image.
    img_points = [60.217477315718455, 24.81593439001388, 60.206147307228015, 24.75203106012519]
    for d in gps_data:
        x1, y1 = scale_to_img(img_points, d, (image.size[0], image.size[1]))  # Convert GPS coordinates to image coordinates.
        img_points.append((x1, y1))
    draw = ImageDraw.Draw(image)
    draw.line(img_points, fill=(255, 0, 0), width=2)  # Draw converted records to the map image.
    image.save('resultMap.png')

data = load_data()
draw_map(data)