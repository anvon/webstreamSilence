from VolumeDetector import VolumeDetector
from multiprocessing import Process


def detect_volume(detector):
    try:
        mean_volume, error = detector.detect_volume()
        if error:
            print(error)
        elif mean_volume is not None:
            print(f"Mean volume: {mean_volume:.2f} dB")
        else:
            print("Unknown error occurred.")
    except Exception as e:
        print(e)


detector1 = VolumeDetector(
    "http://radiocentral.ice.infomaniak.ch/radiocentral-128.mp3", -35, 20)
detector2 = VolumeDetector(
    "http://radiocentral.ice.infomaniak.ch/radiocentral-128.mp3", -40, 21)

p1 = Process(target=detect_volume, args=(detector1,))
p2 = Process(target=detect_volume, args=(detector2,))

p1.start()
p2.start()

p1.join()
p2.join()
