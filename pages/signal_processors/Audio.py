import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
from scipy.io import wavfile
from sections.signal_processing.fast_fourier import frankie_fft
from sections.signal_processing.fast_WH import frankie_WH, mark_WH
import os, sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

st.set_page_config(page_title="Audio FFT/WHT")


def main():
    st.title("Audio Fourier/Walsh Transformer")

    file = st.file_uploader("Upload Audio file (must be .wav): ", type=["wav"])
    if file is None:
        st.info("Upload a .wav file to see its spectrum.")
        return

    # Read audio
    sample_rate, data = wavfile.read(file)

    # Stereo → mono
    if data.ndim == 2:
        data = data.mean(axis=1)

    # Convert to float in [-1, 1]
    if np.issubdtype(data.dtype, np.integer):
        max_val = np.iinfo(data.dtype).max
        data = data.astype(np.float32) / max_val
    else:
        data = data.astype(np.float32)

    n_samples = len(data)
    if n_samples == 0:
        st.error("Audio file appears to be empty.")
        return

    duration = n_samples / sample_rate

    st.write(
        f"Sample rate: **{sample_rate} Hz**, "
        f"duration: **{duration:.2f} s**, "
        f"samples: **{n_samples}**"
    )

    # ---- Use a power-of-two length for transforms ----
    N = 1 << (n_samples.bit_length() - 1)  # largest power of 2 <= n_samples
    if N != n_samples:
        st.info(f"Using first {N} samples (nearest power of 2) for FFT/Walsh transform.")
    data_fft = data[:N]

    # ---- Time-domain plot (use original data, maybe truncated for speed) ----
    max_samples_time_plot = 5000
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

    # 🔧 Transformation selection
    method = st.selectbox("Choose a transformation:", ["Fast Fourier", "Walsh Hadamard"])

    st.subheader("Magnitude spectrum |X(f)| of audio")

    X = None  # will hold the transform result

    if method == "Fast Fourier":
        member = st.selectbox("Choose a group member's function:", ["Francis"])
        if member == "Francis":
            # Frankie FFT on length-N data
            X = frankie_fft.fast_fourier_transform(data_fft)

    else:  # Walsh Hadamard
        member = st.selectbox("Choose a group member's function:", ["Francis", "Mark"])
        if member == "Francis":
            X = frankie_WH.HadamardWalsh2(data_fft, N)
        else:  # Mark
            X = mark_WH.hadamardWalsh2(data_fft, N)

    if X is None:
        st.error("No transform result available. Check that your transform functions are implemented correctly.")
        return

    # --- Frequency axis construction, using N (same as data_fft length) ---
    freqs = np.zeros(N)
    for k in range(N):
        if k <= N // 2:
            freqs[k] = k * sample_rate / N
        else:
            freqs[k] = (k - N) * sample_rate / N

    # Keep only positive frequencies (0 → Nyquist)
    mask = freqs >= 0
    freqs = freqs[mask]
    X = X[mask]

    # ---- Magnitude spectrum on dB scale ----
    mag = np.abs(X)

    # Normalize so the max bin is 0 dB
    if mag.max() > 0:
        mag = mag / mag.max()
    mag_db = 20 * np.log10(mag + 1e-12)  # avoid log(0)

    df_fft = pd.DataFrame({
        "frequency": freqs,
        "magnitude_db": mag_db
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
        y=alt.Y(
            "magnitude_db:Q",
            title="|X(f)| (dB)",
            scale=alt.Scale(domain=[-140, 0])  # or whatever min you want
        )
    )
    .properties(height=300)
)


    st.altair_chart(chart_fft, use_container_width=True)


if __name__ == "__main__":
    main()
