import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
from scipy.io import wavfile  # ✅ correct import
from sections.signal_processing.fast_fourier import frankie_fft
from sections.signal_processing.fast_WH import frankie_WH, mark_WH
import os, sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

st.set_page_config(page_title="Audio Processor")

def main():
    st.title("Audio Fourier/Walsh Transformer")

    file = st.file_uploader("Upload Audio file (must be .wav): ", type=["wav"])
    if file is None:
        st.info("Upload a .wav file to see its spectrum.")
        return
    sample_rate, data = wavfile.read(file)

    # Stereo → mono
    if data.ndim == 2:
        data = data.mean(axis=1)

    # Convert to float
    if np.issubdtype(data.dtype, np.integer):
        max_val = np.iinfo(data.dtype).max
        data = data.astype(np.float32) / max_val
    else:
        data = data.astype(np.float32)

    max_samples_time_plot = 5000
    n_samples = len(data)
    duration = n_samples / sample_rate

    st.write(
        f"Sample rate: **{sample_rate} Hz**, "
        f"duration: **{duration:.2f} s**, "
        f"samples: **{n_samples}**"
    )

    # Time vector (for plotting, maybe truncate)
    if n_samples > max_samples_time_plot:
        show_data = data[:max_samples_time_plot]
        t = np.arange(max_samples_time_plot) / sample_rate
    else:
        show_data = data
        t = np.arange(n_samples) / sample_rate

    df_time = pd.DataFrame({
        "t": t,
        "x(t)": show_data
    })

    st.subheader("Time-domain waveform")

    chart_time = (
        alt.Chart(df_time)
        .mark_line()
        .encode(
            x=alt.X("t:Q", title="t (seconds)"),
            y=alt.Y("x(t):Q", title="Amplitude")
        )
        .properties(height=300)
    )

    st.altair_chart(chart_time, use_container_width=True)

    # Play audio
    st.audio(file)
    method = st.select_box("Choose a tranformation: ",["Fast Fourier", "Walsh Hadamard"])
    # FFT (one-sided, real-valued)
    
    st.subheader("Magnitude spectrum |X(f)| of audio")

    if method == "Fast Fourier":
        member = st.selectbox("Choose a group members function: ", ["Francis","Mark"])
        if member == "Frankie":
            X = frankie_fft.fast_fourier_transform(data)
        else: #Mark
            st.error("Still need Mark's function: ")
    else: # Walsh Hadamard
        member = st.selectbox("Choose a group members function: ", ["Francis","Mark"])
        if member == "Francis":
            X = frankie_WH.wa

        
        

    else:
        X = fr
    # Full frequency array
    N = len(data)
    freqs = np.zeros(N)
    for k in range(N):
        if k <= N//2:
            freqs[k] = k * sample_rate / N
        else:
            freqs[k] = (k - N) * sample_rate / N

    # Keep only positive frequencies (0 → Nyquist)
    mask = freqs >= 0
    freqs = freqs[mask]
    X = X[mask]

    # Magnitude spectrum
    mag = np.abs(X)


    df_fft = pd.DataFrame({
        "frequency": freqs,
        "magnitude": mag
    })

    max_plot_freq = st.slider(
        "Max frequency to display (Hz)",
        min_value=1000,
        max_value=int(sample_rate // 2),
        value=min(20000, int(sample_rate // 2))
    )

    df_fft_plot = df_fft[df_fft["frequency"] <= max_plot_freq]

    chart_fft = (
        alt.Chart(df_fft_plot)
        .mark_line()
        .encode(
            x=alt.X("frequency:Q", title="Frequency (Hz)"),
            y=alt.Y("magnitude:Q", title="|X(f)|")
        )
        .properties(height=300)
    )

    st.altair_chart(chart_fft, use_container_width=True)

if __name__ == "__main__":
    main()
