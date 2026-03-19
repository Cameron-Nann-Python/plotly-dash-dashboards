# Audio Dashboard

![Audio Dashboard Desktop View](https://github.com/Cameron-Nann-Python/plotly-dash-dashboards/blob/main/basic_audio_dashboard/screenshots/audio_dashboard_desktop.png)

## Overview
The purpose of this dashboard was to explore audio wave data with librosa. A sound clip was extracted from the Librosa collection and graphs of the waveform, Fast Fourier Transform (FFT), and Mel spectrogram were produced. The graphs are interactive and respond to a time slider input representing the duration of the audio clip in seconds. The graphs support cross-filter zooming with the relayoutData feature in Dash, and the dashboard supports deskop and tablet views.

## App Layout

### Time Slider
The duration of the audio clip.

### Waveform Graph
The raw audio data

### FFT Graph
The frequency of spanding the selected time frame

### Mel Spectrogram
The range of frequency in decibels of the elapsed time period

## Tablet View
The follwing image shows the dashboard view on a tablet:
![Audio Dashboard Tablet View](https://github.com/Cameron-Nann-Python/plotly-dash-dashboards/blob/main/basic_audio_dashboard/screenshots/audio_dashboard_tablet.png)

## Recommendations
To enhance the dashboard, audio playback could be installed so that the audio clip can be heard when manipulation the time slider. To have a functional dashboard on phones, the slider ticks would have to be modified and the plots would need tighter constraints. 

## Files Included
- `audio_dashboard.py`: Python file containing full dashboard logic
- `requirements.txt`: List of Python dependencies needed for dashboard
- `audio_dashboard_desktop.png`: Screenshot of desktop view
- `audio_dashboard_desktop.png`: Screenshow of tablet view
- `Procfile`: Establish connection to Render
