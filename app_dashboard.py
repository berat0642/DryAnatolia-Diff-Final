
import streamlit as st
import xarray as xr
import matplotlib.pyplot as plt
import imageio
import io
import os

st.set_page_config(layout="wide")
st.title("📊 DryAnatolia-Diff: Kuraklık Dashboard")

# NetCDF dosyasını yükle veya örnek veri kullan
uploaded_file = st.file_uploader("NetCDF dosyanızı yükleyin (.nc)", type=["nc"])
default_path = "data/dryanatolia_sample_grid_2023.nc"

if uploaded_file is not None:
    try:
        uploaded_file.seek(0)
        ds = xr.open_dataset(io.BytesIO(uploaded_file.read()), engine="netcdf4")
    except Exception as e:
        st.error(f"File could not be opened: {e}")
        st.stop()
else:
    st.info("Please upload a NetCDF (.nc) file to begin.")
    st.stop()


# Layout: 2 kolon (sol: animasyon, sağ: detay harita)
col1, col2 = st.columns(2)

if uploaded_file:
    ds = xr.open_dataset(io.BytesIO(uploaded_file.read()))
else:
    if os.path.exists(default_path):
        ds = xr.open_dataset(default_path)
    else:
        st.error("Veri bulunamadı.")
        st.stop()

# Zaman ve değişken seçimi
var_name = list(ds.data_vars)[0]
times = ds.coords["time"].values
selected_time = st.slider("Tarih Seçin", 0, len(times) - 1, 6, format="%d", key="time_slider")
current_time = str(times[selected_time])[:10]

# Sol Panel: Animasyon
with col1:
    st.subheader("🌀 Yıllık Kuraklık Haritası Animasyonu")
    images = []
    for i, t in enumerate(times):
        fig, ax = plt.subplots(figsize=(5, 3))
        ds[var_name].sel(time=t).plot(ax=ax, cmap="coolwarm", vmin=-3, vmax=3, add_colorbar=False)
        ax.set_title(str(t)[:10])
        ax.set_axis_off()
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        images.append(imageio.v2.imread(buf))
        plt.close(fig)
    gif_bytes = io.BytesIO()
    imageio.mimsave(gif_bytes, images, format="GIF", duration=1.0)
    st.image(gif_bytes.getvalue(), caption="2023 Kuraklık Animasyonu (DSI)", use_container_width=True)
    st.download_button("🎞️ Animasyonu İndir (GIF)", gif_bytes.getvalue(), file_name="dsi_animation.gif", mime="image/gif")

# Sağ Panel: Seçili Tarih Haritası
with col2:
    st.subheader(f"📍 {current_time} için Kuraklık Haritası")
    fig, ax = plt.subplots(figsize=(6, 4))
    ds[var_name].sel(time=times[selected_time]).plot(ax=ax, cmap="coolwarm", vmin=-3, vmax=3)
    ax.set_title(f"{current_time} – {var_name}")
    st.pyplot(fig)

    # PNG olarak indirme
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button("🖼️ Haritayı İndir (PNG)", data=buf.getvalue(), file_name=f"dsi_{current_time}.png", mime="image/png")
