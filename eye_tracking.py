import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
import numpy

def clean(fileName):
  # Assuming data is your list of dictionaries
  file = open(fileName, 'r')

  data = json.load(file)

  # Filter python objects with list comprehensions
  output = [x['afe'][0:2] for x in data]
  file.close()
  return output
  # Transform python object back into json
  outputJson = json.dumps(output)

  # Show json
  # print(outputJson)

  out = open('./out.json', 'w');

  out.write(outputJson)
  return outputJson

def combine():
  f1 = clean('./Driving/Participant_1/AFE_000_CONFIDENTIAL.json')
  f2= clean('./Driving/Participant_1/AFE_001_CONFIDENTIAL.json')
  f3 = clean('./Driving/Participant_1/AFE_002_CONFIDENTIAL.json')
  f4= clean('./Driving/Participant_1/AFE_003_CONFIDENTIAL.json')
  dataOut = json.dumps(f1+f2+f3+f4)
  out = open('./out.json', 'w')
  out.write(dataOut)

def plot(data, delta, anomalies = []):
   # Assuming data is your list of dictionaries
  # file = open(fileName, 'r')

  # data = json.load(file)

  # Extract the left and right eye movements
  left = []
  for i in range(0,6):
    left.append([d[0]['m'][0][i] for d in data])
  ticktimes = [(d[0]['i'][0] - data[0][0]['i'][0])/1000 for d in data]
  
  right = []
  for i in range(0,6):
    right.append([d[1]['m'][0][i] for d in data])

  # Create the plot
  fig = plt.figure(figsize=(10, 5))

  # Plot the left eye movements
  # for index, sensor in enumerate(left):
  #   plt.plot(ticktimes, sensor, label='Left Eye Sensor ' + str(index))

  # for index, sensor in enumerate(right):
  #   plt.plot(ticktimes, sensor, label='Right Eye Sensor ' + str(index))

  # interval = 5*60
  # i = interval
  # averageOverInterval = []
  # averageTickTimes = []
  # while i < len(delta):
  #   j = 0
  #   average = 0
  #   while j < interval:
  #     average += delta[i-j]
  #     j += 1
  #   averageOverInterval.append(average/interval)
  #   averageTickTimes.append(ticktimes[i])
  #   i += interval

  # plt.plot(averageTickTimes, averageOverInterval, label='Average Eye Movement Delta Past 5s')
  for i in anomalies:
    s, e = i
    plt.axvspan(s, e, color='red', alpha=0.5, lw=0)

  # Add a legend
  plt.legend()

  def animate(i):
    plt.clf()
    # Plot the left eye movements
    # for index, sensor in enumerate(left):
    #     plt.plot(ticktimes[:i], sensor[:i], label='Left Eye Sensor ' + str(index))

    # for index, sensor in enumerate(right):
    #   plt.plot(ticktimes[:i], sensor[:i], label='Right Eye Sensor ' + str(index))

    plt.plot(ticktimes[i:i+1000], delta[i:i+1000], label='Eye Movement')

    for s, e in anomalies:
      if s < ticktimes[i+1000] and s > ticktimes[i]:
        plt.axvspan(s, min(e, ticktimes[i + 1000]), color='red', alpha=0.5, lw=0)

    # Add a legend
    plt.legend()

  ani = animation.FuncAnimation(fig, animate, frames=numpy.arange(0, len(delta), 10), repeat=True, interval=1)

  # Show the plot
  plt.show()

def get_sensor_average_absolute_delta(data):
  delta = []
  prev = None
  for index, curr in enumerate(data):
    if index == 0:
      prev = curr
      delta.append(0)
    else:
      deltaSum = 0
      for j in range(len(curr)):
        deltaSum += abs(curr[j]-prev[j])
      delta.append(deltaSum/len(curr))
      prev = curr
  return delta

def group_continuous_integers(arr):
  if not arr:
    return []

  ranges = []
  start = arr[0]
  end = arr[0]

  for num in arr[1:]:
    if num == end + 1:
      end = num
    else:
      ranges.append((start, end))
      start = end = num

  ranges.append((start, end))
  return ranges


def get_anomalies(delta, frameSize, minDelta):
  anomalies = []
  i=frameSize
  while i < len(delta):
    j = 0
    outliers = 0
    while j < frameSize:
      if abs(delta[i-j]) > minDelta:
        outliers += 1
      j += 1
    if outliers < frameSize*0.005:
      anomalies.append(i)
    i += 1
  return anomalies

def get_common_subset(set_array):
  common_subset = set(set_array[0])
  for ranges in set_array[1:]:
    new_common_subset = set()
    for common_range in common_subset:
      for range_ in ranges:
        # Check for overlap
        if common_range[1] >= range_[0] and common_range[0] <= range_[1]:
          new_common_subset.add((max(common_range[0], range_[0]), min(common_range[1], range_[1])))
    common_subset = new_common_subset
  return common_subset

def analyze(frameSize=200, minDelta=400):
  f1 = clean('./data/driving_1/AFE_000_CONFIDENTIAL.json')
  f2 = clean('./data/driving_1/AFE_001_CONFIDENTIAL.json')
  f3 = clean('./data/driving_1/AFE_002_CONFIDENTIAL.json')
  f4 = clean('./data/driving_1/AFE_003_CONFIDENTIAL.json')
  data = f1+f2+f3+f4

  sensor_data = []
  for i in data:
    combined_sensor_data = []
    for j in range(0,6):
      combined_sensor_data.append(i[0]['m'][0][j])
      combined_sensor_data.append(i[1]['m'][0][j])
    sensor_data.append(combined_sensor_data)

  sensor_delta = get_sensor_average_absolute_delta(sensor_data)

  sensor_anomalies = group_continuous_integers(get_anomalies(sensor_delta, frameSize, minDelta))
  # sensor_anomalies_right = get_anomalies(sensors_right, frameSize, minDelta)

  # common_subset = get_common_subset([
  #   group_continuous_integers(sensor_anomalies_left),
  #   group_continuous_integers(sensor_anomalies_right)
  # ])

  tickOffset = data[0][0]['i'][0]
  anomalies = []
  for i in sensor_anomalies:
    start, end = i
    if end-start < frameSize*0.99:
      continue
    anomalies.append(((data[start][0]['i'][0] - tickOffset)/1000, (data[end][0]['i'][0] - tickOffset)/1000))

  plot(data, sensor_delta, anomalies)

def analyze_by_path(frameSize=200, minDelta=400, path='CWD'):
  f1 = clean(path + '/AFE_000_CONFIDENTIAL.json')
  f2 = clean(path + '/AFE_001_CONFIDENTIAL.json')
  f3 = clean(path + '/AFE_002_CONFIDENTIAL.json')
  f4 = clean(path + '/AFE_003_CONFIDENTIAL.json')
  data = f1+f2+f3+f4

  sensor_data = []
  for i in data:
    combined_sensor_data = []
    for j in range(0,6):
      combined_sensor_data.append(i[0]['m'][0][j])
      combined_sensor_data.append(i[1]['m'][0][j])
    sensor_data.append(combined_sensor_data)

  sensor_delta = get_sensor_average_absolute_delta(sensor_data)

  sensor_anomalies = group_continuous_integers(get_anomalies(sensor_delta, frameSize, minDelta))
  # sensor_anomalies_right = get_anomalies(sensors_right, frameSize, minDelta)

  # common_subset = get_common_subset([
  #   group_continuous_integers(sensor_anomalies_left),
  #   group_continuous_integers(sensor_anomalies_right)
  # ])

  tickOffset = data[0][0]['i'][0]
  anomalies = []
  for i in sensor_anomalies:
    start, end = i
    if end-start < frameSize*0.99:
      continue
    anomalies.append(((data[start][0]['i'][0] - tickOffset)/1000, (data[end][0]['i'][0] - tickOffset)/1000))

  plot(data, sensor_delta, anomalies)

def analyze_single_datafile_by_path(frameSize=200, minDelta=400, path='CWD'):
  f1 = clean(path)
  data = f1

  sensor_data = []
  for i in data:
    combined_sensor_data = []
    for j in range(0,6):
      combined_sensor_data.append(i[0]['m'][0][j])
      combined_sensor_data.append(i[1]['m'][0][j])
    sensor_data.append(combined_sensor_data)

  sensor_delta = get_sensor_average_absolute_delta(sensor_data)

  sensor_anomalies = group_continuous_integers(get_anomalies(sensor_delta, frameSize, minDelta))
  # sensor_anomalies_right = get_anomalies(sensors_right, frameSize, minDelta)

  # common_subset = get_common_subset([
  #   group_continuous_integers(sensor_anomalies_left),
  #   group_continuous_integers(sensor_anomalies_right)
  # ])

  tickOffset = data[0][0]['i'][0]
  anomalies = []
  for i in sensor_anomalies:
    start, end = i
    if end-start < frameSize*0.99:
      continue
    anomalies.append(((data[start][0]['i'][0] - tickOffset)/1000, (data[end][0]['i'][0] - tickOffset)/1000))

  plot(data, sensor_delta, anomalies)
# clean('./Driving/Participant_1/AFE_000_CONFIDENTIAL.json')
# combine()
# plot('./driving_participant1.json')
def get_issue_areas(path, frameSize=200, minDelta=400):
  f1 = clean(path + '/AFE_000_CONFIDENTIAL.json')
  f2 = clean(path + '/AFE_001_CONFIDENTIAL.json')
  f3 = clean(path + '/AFE_002_CONFIDENTIAL.json')
  f4 = clean(path + '/AFE_003_CONFIDENTIAL.json')
  data = f1+f2+f3+f4

  sensor_data = []
  for i in data:
    combined_sensor_data = []
    for j in range(0,6):
      combined_sensor_data.append(i[0]['m'][0][j])
      combined_sensor_data.append(i[1]['m'][0][j])
    sensor_data.append(combined_sensor_data)

  sensor_delta = get_sensor_average_absolute_delta(sensor_data)

  return group_continuous_integers(get_anomalies(sensor_delta, frameSize, minDelta))

def get_issue_areas_standalone(path, frameSize=200, minDelta=400):
  f1 = clean(path)
  data = f1

  sensor_data = []
  for i in data:
    combined_sensor_data = []
    for j in range(0,6):
      combined_sensor_data.append(i[0]['m'][0][j])
      combined_sensor_data.append(i[1]['m'][0][j])
    sensor_data.append(combined_sensor_data)

  sensor_delta = get_sensor_average_absolute_delta(sensor_data)

  return group_continuous_integers(get_anomalies(sensor_delta, frameSize, minDelta))

def eye_analysis(path):
  analyze_single_datafile_by_path(path=path)
#analyze()
#analyze_by_path(path = 'data/driving_1')
