import subprocess

VOLUME_THRESHOLD = -30
STREAM_URL = "http://radiocentral.ice.infomaniak.ch/radiocentral-128.mp3"
DURATION = 15

command = [
    "ffmpeg",
    "-i",
    STREAM_URL,
    "-filter_complex",
    "[a]volumedetect",
    "-t",
    str(DURATION),
    "-f",
    "null",
    "-"
]

try:
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e.output}")
else:
    mean_volume = None

    for line in iter(process.stdout.readline, b''):
        if "mean_volume" in line:
            mean_volume = float(line.split("mean_volume: ")[1].rstrip(" dB\n"))
            print(f"Current volume: {mean_volume:.2f} dB")
            if mean_volume < VOLUME_THRESHOLD:
                print("Silence detected.")
        if mean_volume and mean_volume >= VOLUME_THRESHOLD:
            break

        # Stop the process after the specified duration
        process.poll()
        if process.returncode is not None:
            break

        if process.returncode is None and process.stdout.fileno() == -1:
            print("Error: Stdout is not valid.")

    process.stdout.close()
    process.wait()
    return_code = process.returncode
    print(f"Process returned with code: {return_code}")
