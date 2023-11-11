import matplotlib.pyplot as plt
import json

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

def plot(data, anomalies = []):
   # Assuming data is your list of dictionaries
  # file = open(fileName, 'r')

  # data = json.load(file)

  # Extract the left and right eye movements
  left = []
  for i in range(0,6):
    left.append([d[0]['m'][0][i] for d in data])
  left_ticktimes = [(d[0]['i'][0] - data[0][0]['i'][0])/1000 for d in data]
  
  right = []
  for i in range(0,6):
    right.append([d[1]['m'][0][i] for d in data])
  right_ticktimes = [(d[1]['i'][0] - data[0][1]['i'][0])/1000 for d in data]

  # Create the plot
  plt.figure(figsize=(10, 5))

  # Plot the left eye movements
  for index, sensor in enumerate(left):
    plt.plot(left_ticktimes, sensor, label='Left Eye Sensor ' + str(index))

  for index, sensor in enumerate(right):
    plt.plot(right_ticktimes, sensor, label='Right Eye Sensor ' + str(index))

  for i in anomalies:
    s, e = i
    plt.axvspan(s, e, color='red', alpha=0.5, lw=0)

  # Add a legend
  plt.legend()

  # Show the plot
  plt.show()

def normalize(data):
  delta = []
  for index, curr in enumerate(data):
    if index == 0:
      delta.append(0)
    else:
      prev = data[index-1]
      delta.append(curr-prev)  
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


def get_anomalies(data, frameSize, minDelta):
  delta = normalize(data)

  anomalies = []
  i=frameSize
  while i < len(delta):
    j = 0
    outliers = 0
    while j < frameSize:
      if abs(delta[i-j]) > minDelta:
        outliers += 1
      j += 1
    if outliers < frameSize*0.01:
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

def analyze(frameSize=125, minDelta=500):
  f1 = clean('./Driving/Participant_1/AFE_000_CONFIDENTIAL.json')
  f2 = clean('./Driving/Participant_1/AFE_001_CONFIDENTIAL.json')
  f3 = clean('./Driving/Participant_1/AFE_002_CONFIDENTIAL.json')
  f4 = clean('./Driving/Participant_1/AFE_003_CONFIDENTIAL.json')
  data = f1+f2+f3+f4
  anomalies = []
  for i in range(0,6):
    sensor_left = [d[0]['m'][0][i] for d in data]
    sensor_right = [d[1]['m'][0][i] for d in data]
    sensor_anomalies_left = get_anomalies(sensor_left, frameSize, minDelta)
    sensor_anomalies_right = get_anomalies(sensor_right, frameSize, minDelta)
    anomalies.append(group_continuous_integers(sensor_anomalies_left))
    anomalies.append(group_continuous_integers(sensor_anomalies_right))

  common_subset = get_common_subset(anomalies)

  tickOffset = data[0][0]['i'][0]
  plotData = []
  for i in common_subset:
    start, end = i
    if end-start < frameSize:
       continue
    plotData.append(((data[start][0]['i'][0] - tickOffset)/1000, (data[end][0]['i'][0] - tickOffset)/1000))
  plot(data, plotData)

# clean('./Driving/Participant_1/AFE_000_CONFIDENTIAL.json')
# combine()
# plot('./driving_participant1.json')
analyze()
