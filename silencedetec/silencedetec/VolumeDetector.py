import subprocess


class VolumeDetector:
    def __init__(self, url, threshold=-30, duration=15):
        self.url = url
        self.threshold = float(threshold)
        self.duration = duration

    def detect_volume(self):
        command = [
            "ffmpeg",
            "-i",
            self.url,
            "-filter_complex",
            "[a]volumedetect",
            "-t",
            str(self.duration),
            "-f",
            "null",
            "-"
        ]

        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error starting FFmpeg: {e.output}")
        else:
            mean_volume = None
            error = None
            print("Start testing")
            for line in iter(process.stdout.readline, b''):
                line = line.decode('utf-8')
                if "mean_volume" in line:
                    mean_volume = float(line.split(
                        "mean_volume: ")[1].rstrip(" dB\n"))
                    print(f"mean volume: {mean_volume:.2f} dB")
                    if mean_volume < self.threshold:
                        print("Silence detected.")
                if mean_volume and mean_volume >= self.threshold:
                    break

                # Stop the process after the specified duration
                process.poll()
                if process.returncode is not None:
                    print("return code not None", mean_volume)
                    break

                if process.returncode is None and process.stdout.fileno() == -1:
                    print("return code not valid.")
                    error = "Error: Stdout is not valid."
                    break

            process.stdout.close()

            process.wait()

            if process.returncode == 0:
                return mean_volume, error
            else:
                raise Exception(
                    f"FFmpeg command failed with exit status {process.returncode}")
