import streamlit as st
import piexif
from PIL import Image
from io import BytesIO
import zipfile
import os

# ---------- Helper Functions ----------

def decimal_to_dms_rational(deg_float):
    deg_abs = abs(deg_float)
    deg = int(deg_abs)
    min_float = (deg_abs - deg) * 60
    minute = int(min_float)
    sec = int((min_float - minute) * 60 * 100)
    return ((deg, 1), (minute, 1), (sec, 100))

def set_gps_location(exif_dict, lat, lng, alt):
    lat_ref = 'N' if lat >= 0 else 'S'
    lng_ref = 'E' if lng >= 0 else 'W'
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = lat_ref.encode()
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = decimal_to_dms_rational(lat)
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = lng_ref.encode()
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = decimal_to_dms_rational(lng)
    exif_dict['GPS'][piexif.GPSIFD.GPSAltitude] = (int(alt * 100), 100)
    exif_dict['GPS'][piexif.GPSIFD.GPSAltitudeRef] = b'\x00'

def convert_to_jpeg(img_file):
    try:
        img = Image.open(img_file).convert("RGB")
    except Exception as e:
        st.error(f"Failed to open image: {e}")
        return None
    new_img_io = BytesIO()
    img.save(new_img_io, format='JPEG')
    new_img_io.seek(0)
    return new_img_io

def geo_tag_image(image_bytes, lat, lng, alt):
    img = Image.open(image_bytes)
    try:
        exif_dict = piexif.load(img.info.get("exif", b""))
    except:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}
    set_gps_location(exif_dict, lat, lng, alt)
    exif_bytes = piexif.dump(exif_dict)
    output = BytesIO()
    img.save(output, "jpeg", exif=exif_bytes)
    output.seek(0)
    return output

# ---------- Streamlit UI ----------

st.set_page_config(page_title="📍 Geo-Tag Images", layout="centered")
st.title("📸 Geo-Tag Your Images")
st.markdown("Upload images and tag them with your GPS coordinates!")

uploaded_files = st.file_uploader(
    "Upload images", 
    accept_multiple_files=True, 
    type=["jpg", "jpeg", "png", "webp"]
)

latitude = st.number_input("Enter Latitude (e.g., 23.8103)", format="%.6f")
longitude = st.number_input("Enter Longitude (e.g., 90.4125)", format="%.6f")
altitude = st.number_input("Enter Altitude in meters (optional)", value=0.0, format="%.2f")

if st.button("✅ Geo-Tag & Download ZIP") and uploaded_files:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for file in uploaded_files:
            filename = os.path.splitext(file.name)[0] + ".jpg"
            jpeg_io = convert_to_jpeg(file)
            if not jpeg_io:
                continue
            tagged_io = geo_tag_image(jpeg_io, latitude, longitude, altitude)
            zipf.writestr(filename, tagged_io.read())
            st.success(f"Tagged: {filename}")
    zip_buffer.seek(0)
    st.download_button("⬇️ Download Geo-Tagged ZIP", zip_buffer, file_name="geo_tagged_images.zip", mime="application/zip")
    st.balloons()
