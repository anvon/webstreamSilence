from django.shortcuts import render
from silencedetec.forms import VolumeDetectorForm

from .VolumeDetector import VolumeDetector


def index(request):
    if request.method == 'POST':
        form = VolumeDetectorForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            threshold = form.cleaned_data['threshold']
            duration = form.cleaned_data['duration']

            detector = VolumeDetector(url, threshold, duration)
            mean_volume, error = detector.detect_volume()

            if error:
                context = {'error': error}
            elif mean_volume is not None:
                context = {'mean_volume': mean_volume}
            else:
                context = {'error': 'Unknown error occurred.'}

            return render(request, 'index.html', context)
    else:
        form = VolumeDetectorForm()

    return render(request, 'index.html', {'form': form})
