
import streamlit as st
import xarray as xr
import matplotlib.pyplot as plt
import io

st.set_page_config(layout="wide")
st.title("🌍 DryAnatolia-Diff: Kuraklık Senaryosu Görselleştirme")

st.markdown("Bu uygulama, koşullu Latent Diffusion modeli tarafından üretilen veya sizin yüklediğiniz NetCDF veriler üzerinden kuraklık haritaları üretir.")

# Veri yükleme
uploaded_file = st.file_uploader("NetCDF dosyanızı yükleyin (.nc)", type=["nc"])

if uploaded_file:
    try:
        ds = xr.open_dataset(uploaded_file)
        variable_options = list(ds.data_vars)
        time_options = ds.coords['time'].values

        st.success("Veri başarıyla yüklendi!")

        # Değişken seçimi
        selected_var = st.selectbox("Görüntülenecek değişken:", variable_options)

        # Tarih seçimi
        selected_time = st.selectbox("Tarih seçin:", time_options)

        # Grid görselleştir
        selected_data = ds[selected_var].sel(time=selected_time)

        st.subheader(f"{selected_time} – {selected_var}")
        fig, ax = plt.subplots(figsize=(7, 5))
        selected_data.plot(ax=ax, cmap="coolwarm", add_colorbar=True)
        ax.set_title(f"{selected_time} – {selected_var}")
        st.pyplot(fig)

        # İndirme
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button("Haritayı İndir (PNG)", data=buf.getvalue(), file_name=f"{selected_var}_{selected_time}.png", mime="image/png")

    except Exception as e:
        st.error(f"Veri işlenemedi: {e}")

else:
    st.info("Alternatif olarak uygulamadaki örnek veriyle devam etmek için herhangi bir dosya yüklemeyin.")
