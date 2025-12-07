import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import os, sys

st.set_page_config(page_title ="Fast Fourier")

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)


from sections.signal_processing.fast_fourier import frankie_fft
#from sections.signal_processing.fast_WH import frankie_WH

def main():
    st.title("Fast Fourier Transformer")
    st.sidebar.header("Signal settings")

    signal_type = st.sidebar.selectbox(
        "Signal template",
        ["Custom", "sin(2*pi*f*t)", "cos(2*pi*f*t)", "exp(-t)*sin(2*pi*f*t)"]
    )

    if signal_type != "Custom":
        expr = signal_type  # override text box with template
    else:
        expr = st.sidebar.text_input(
            "Custom x(t) =",
            value="sin(2*pi*f*t)"
        )

    f = st.sidebar.number_input("Frequency f (Hz)", value=5.0)
    T = st.sidebar.number_input("Duration T (seconds)", value=1.0)
    N = st.sidebar.selectbox("Number of samples N", [32, 64, 128, 256, 512], index=2)


    t = np.linspace(0, T, N, endpoint=False)

    local_ns = {
        "t": t,
        "f": f,
        "pi": np.pi,
        "sin": np.sin,
        "cos": np.cos,
        "exp": np.exp,
        "sqrt": np.sqrt,
    }

    try:
        x = eval(expr, {"__builtins__": {}}, local_ns)
        error = None
    except Exception as e:
        x = None
        error = str(e)


    if error:
        st.error(f"Could not evaluate expression:\n{error}")

    else:
        df_time = pd.DataFrame({
            "t": t,
            "x(t)": x
        })

        st.subheader("Time-domain signal x(t)")

        chart_time = (
            alt.Chart(df_time)
            .mark_line(point=True)
            .encode(
                x=alt.X("t:Q", title="t (seconds)"),
                y=alt.Y("x(t):Q", title="x(t)")
            )
            .properties(height=300)
        )

        st.altair_chart(chart_time, use_container_width=True)

        st.subheader("FFT magnitude spectrum |X(f)|")

        X = frankie_fft.fast_fourier_transform(x)
        freqs = np.fft.fftfreq(N, d=T/N)

        df_fft = pd.DataFrame({
            "frequency": freqs,
            "magnitude": np.abs(X)
        })

        chart_fft = (
            alt.Chart(df_fft)
            .mark_bar()
            .encode(
                x=alt.X("frequency:Q", title="Frequency (Hz)"),
                y=alt.Y("magnitude:Q", title="|X(f)|")
            )
            .properties(height=300)
        )

        st.altair_chart(chart_fft, use_container_width=True)

if __name__ == "__main__":
    main()