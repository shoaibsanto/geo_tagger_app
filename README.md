# 📍 Geo Tagger App

A simple Streamlit web app that allows users to **upload images and geo-tag them** with latitude, longitude, and altitude coordinates. The processed images are downloaded as a ZIP file with embedded GPS metadata.

---

## 🚀 Features

- Upload multiple images at once
- Supports JPG, PNG, HEIC, and WebP formats (auto-converted to JPEG)
- Input GPS coordinates (latitude, longitude, altitude)
- Embed location data into images using EXIF
- Download all geo-tagged images in a single ZIP file

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) - Frontend and UI
- [Pillow](https://python-pillow.org/) - Image processing
- [piexif](https://github.com/hMatoba/Piexif) - EXIF metadata editing

---

## 📦 Installation

Clone the repo:

```bash
git clone https://github.com/shoaibsanto/geo_tagger_app.git
cd geo_tagger_app
