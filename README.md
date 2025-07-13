
# DryAnatolia-Diff: Kuraklık Senaryosu Üretim Projesi

Bu proje, Güneydoğu Anadolu Bölgesi için 2030-2050 yılları arasında olası kuraklık senaryolarını üretmek amacıyla Koşullu Latent Diffusion modeli ile geliştirilmiştir.

## İçerik
- `app.py`: Gelişmiş Streamlit arayüzü (tek tarihli görselleştirme)
- `app_dashboard.py`: Dashboard görünümü (animasyon + detay harita)
- `DryAnatolia-Diff_Report.pdf`: Tam proje raporu
- `DryAnatolia-Diff_Poster.pdf`: A3 boyutunda poster sunumu
- `DSI_Animation_2023.gif`: 2023 yılına ait DSI animasyonu
- `data/`: NetCDF veri örneği
- `notebooks/`: Görselleştirme için Jupyter dosyaları

## Çalıştırmak için
```bash
pip install -r requirements.txt
streamlit run app_dashboard.py
```

## Deploy
Streamlit Cloud üzerinden bu projeyi deploy etmek için:
1. GitHub reposu oluşturun
2. Yukarıdaki dosyaları yükleyin
3. https://streamlit.io/cloud adresinden yeni app açarak deploy edin

