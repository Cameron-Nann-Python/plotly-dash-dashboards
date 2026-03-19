# Audio Dashboard

![Audio Dashboard Desktop View](https://github.com/Cameron-Nann-Python/plotly-dash-dashboards/blob/main/basic_audio_dashboard/screenshots/audio_dashboard_desktop.png)

## Overview
This dashboard explores audio wave data with librosa. A sound clip was extracted from the Librosa collection and visualized with three interactive plots:
- Waveform
- Fast Fourier Transform (FFT)
- Mel Spectrogram

## Features
- Graphs dynamically respond to a time slider input
- Graphs support cross-filter zooming with the relayoutData feature in Dash
- Dashboard supports desktop and tablet views

## App Layout

### Time Slider
The duration of the audio clip.

### Waveform Graph
The raw audio data over the audio duration

### FFT Graph
- Frequency (Hz) in log-scale spanning the selected time frame
 
### Mel Spectrogram
- Frequency intensity (dB) over the elapsed time period

## Tablet View
The following image shows the dashboard view on a tablet:
![Audio Dashboard Tablet View](https://github.com/Cameron-Nann-Python/plotly-dash-dashboards/blob/main/basic_audio_dashboard/screenshots/audio_dashboard_tablet.png)

## HuggingFace Link
The dashboard can be viewed on HuggingFace Spaces with the following link:

https://huggingface.co/spaces/Cameron-Nann/Audio_Dashboard 

_Note: the callbacks on HuggingFace take time to respond (~5-30s), so run locally for best results._ 

## Technologies Used
- Python (3.12+)
- Dash for interactive UI
- Plotly for data visualization
- Librosa for audio data
- NumPy/Pandas for data handling
- Docker for containerized deployment
- HuggingFace Spaces to host live demo
  
## License
This project is licensed under the MIT License.
  
## Recommendations
- To enhance the dashboard, audio playback could be installed so that the audio clip can be heard when manipulation the time slider.
- To have a functional dashboard on phones, the slider ticks would have to be modified and the plots would need tighter constraints.

## Files Included
- `app.py`: Python file containing full dashboard logic
- `requirements.txt`: List of Python dependencies needed for dashboard
- `audio_dashboard_desktop.png`: Screenshot of desktop view
- `audio_dashboard_tablet.png`: Screenshot of tablet view
