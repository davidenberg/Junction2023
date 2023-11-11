import sys
from accelerometer_tracking import acc_analysis
from eye_tracking import eye_analysis
from gps_mapping import draw_map_standalone

def main():
    if len(sys.argv) < 3:
        print("usage: main.py path-to-afe-datafile path-to-imu-datafile")
        sys.exit()

    eye_analysis(sys.argv[1])
    acc_analysis(sys.argv[2])
    save_map = input("Export map (y/n): ")
    mapname = ""
    count = 0
    while True:
        try:
            if save_map.lower() =='y':
                save_map = True
                mapname = input("Enter name to save: ")
                break
            elif save_map.lower() == 'n':
                save_map = False
                break
            else:
                count += 1
                if count >= 4:
                    sys.exit()
                save_map = input("Export map (y/n): ")
        except:
            count += 1
            if count >= 4:
                sys.exit()
            input("Export map (y/n): ")

    draw_map_standalone(mapname, sys.argv[1], sys.argv[2], save_map)

if __name__ == "__main__":
    main()