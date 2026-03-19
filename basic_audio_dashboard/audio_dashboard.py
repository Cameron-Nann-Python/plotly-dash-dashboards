import librosa

import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

import dash
from dash import dcc, html, callback_context
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

# set plotly theme
pio.templates.default = "plotly_dark"

# load audio with librosa
y, sr = librosa.load(librosa.ex('choice'))

# time slider
time = np.linspace(0, len(y)/sr, len(y))

# Instantiate dash app
app = dash.Dash(
    __name__,
    # Set Bootstrap theme
    external_stylesheets=[dbc.themes.SLATE],
    # Allow app to work for mobile
    meta_tags=[{'name':'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
    )

# App layout
app.layout = dbc.Container([
    # Dashboard title
    dbc.Row([
        dbc.Col([
            html.H1('Audio Dashboard', style={'fontsize':20, 
                                              'color':'#0041C2',
                                              'textAlign':'center'})

        ], width={'size':12})
    ]),
    # Time slider
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Audio Time", style={'color':'white'}),
                dbc.CardBody([
                    dcc.Slider(
                        id='time-slider',
                        min=np.min(time),
                        max=int(np.max(time)),
                        value=25,
                        marks={
                            sec: {
                                'label':f'{sec}s',
                                'style':{'color':'white'}
                            } for sec in range(0, int(np.max(time)+1))
                        },
                    )
                ])
            ], class_name='mb-4 shadow')
        ], width={'size':12}),
    ]),
    # Plots
    dbc.Row([

        dbc.Col([
            # Raw data
            dbc.Card([
                dbc.CardHeader('Waveform', style={'color':'white'}),
                dbc.CardBody([
                    dcc.Graph(id='raw-data', figure={}),
                ])
            ], class_name='mb-4 shadow'),

            # Spectrogram
            dbc.Card([
                dbc.CardHeader('Mel Spectrogram', style={'color':'white'}),
                dbc.CardBody([
                    dcc.Graph(id='spec-data', figure={})
                ])
            ], class_name='mb-4 shadow')
        ], xs=12, sm=12, md=6, xl=6),
        dbc.Col([
            # FFT data
            dbc.Card([
                dbc.CardHeader('FFT', style={'color':'white'}),
                dbc.CardBody([
                    dcc.Graph(id='fft-data', figure={})
                ])
            ], class_name='mb-4 shadow')
        ], xs=12, sm=12, md=6, xl=6)
    ])
], fluid=True)

# Graph callback decorator
@app.callback(
    [
        Output(component_id='raw-data', component_property='figure'),
        Output(component_id='fft-data', component_property='figure'),
        Output(component_id='spec-data', component_property='figure')
    ],
    [
        Input(component_id='time-slider', component_property='value'),
        Input(component_id='raw-data', component_property='relayoutData'),
        Input(component_id='spec-data', component_property='relayoutData')
    ]
)

# Graph callback function
def make_plots(entered_time, raw_relay, spec_relay):

    # Create a callback trigger
    trigger = callback_context.triggered_id

    # Default time bounds
    x0, x1 = None, None

    # Get default waveform
    duration = len(y) / sr
    time = np.linspace(0, duration, len(y))
    amplitude = y

    # Update waveform based on spectrogram zoom
    if trigger == 'spec-data' and 'xaxis.range[0]' in spec_relay:

        # Get zoomed time start and end interval
        x0 = spec_relay.get('xaxis.range[0]')
        x1 = spec_relay.get('xaxis.range[1]')
        if x0 is not None and x1 is not None:
            # Make zoomed indices
            x0_ind = int(x0 * sr)
            x1_ind = int(x1 * sr)

            # Slice the amplitude
            amplitude = y[x0_ind:x1_ind]

            # Update time
            time = np.linspace(x0, x1, len(amplitude))

    # Update spectrogram based on waveform zoom
    if trigger == 'raw-data' and 'xaxis.range[0]' in raw_relay:

        # Get zoomed time start and end interval
        x0 = raw_relay.get('xaxis.range[0]')
        x1 = raw_relay.get('xaxis.range[1]')
        if x0 is not None and x1 is not None:
            # Make zoomed indices
            x0_ind = int(x0 * sr)
            x1_ind = int(x1 * sr)

            # Slice the amplitude
            amplitude = y[x0_ind:x1_ind]

            # Update time
            time = np.linspace(x0, x1, len(amplitude))

    # Create a raw data frame
    df_raw = pd.DataFrame({'Amplitude':amplitude, 'Time':time})

    # Return raw data graph up to specified time
    df_raw_slice = df_raw[df_raw['Time'] <= entered_time]

    # Raw data plot
    raw_fig = px.scatter(
        x=df_raw_slice['Time'],
        y=df_raw_slice['Amplitude']
    )
    raw_fig.update_layout(
        xaxis_title='Time (s)',
        yaxis_title = 'Amplitude',
    )

    # Get FFT data
    y_centered = amplitude - np.mean(amplitude)
    N = len(y_centered)

    if N > 0:
        # Keep only positive frequencies
        fft_vals = np.fft.rfft(y_centered)
        fft_vals = np.abs(fft_vals)
        fft_freqs = np.fft.rfftfreq(N, 1/sr)
    else:
        fft_vals = []
        fft_freqs = []

    # Make a FFT data frame
    fft_data = pd.DataFrame({'Frequency':fft_freqs, 'Magnitude':fft_vals})

    # fft plot
    fft_fig = px.scatter(
        x=fft_data['Frequency'],
        y=fft_data['Magnitude'],
        log_y=True
    )
    fft_fig.update_layout(
        xaxis_title='Frequency (Hz)',
        yaxis_title='Magnitude (log scale)',
    )

    # Mel spectrogram
    S = librosa.feature.melspectrogram(y=amplitude, sr=sr, n_mels=128)

    # Convert to db
    S_db_mel = librosa.power_to_db(S, ref=np.max)

    # Get time based on slider
    full_mel_times = librosa.frames_to_time(np.arange(S_db_mel.shape[1]), sr=sr)
    mel_time_mask = full_mel_times <= entered_time
    mel_times = full_mel_times[mel_time_mask]

    S_db_mel = S_db_mel[:, mel_time_mask]

    # Get frequency
    mel_freqs = librosa.mel_frequencies(n_mels=S_db_mel.shape[0], fmin=0, fmax=sr/2)

    # Plot the Mel spectrogram
    mel_fig = go.Figure(data=go.Heatmap(
        z=S_db_mel,
        x=mel_times,
        y=mel_freqs,
        colorscale='Viridis',
        colorbar=dict(title='dB')
    ))
    mel_fig.update_layout(
        xaxis_title='Time Elasped (s)',
        yaxis_title='Frequency (Hz)',
        yaxis_type='log',
    )

    return[raw_fig.to_dict(), fft_fig.to_dict(), mel_fig.to_dict()]

# Run app
if __name__ == '__main__':
    app.run()
