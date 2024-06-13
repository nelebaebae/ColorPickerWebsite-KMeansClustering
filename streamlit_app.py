import streamlit as st
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

st.set_page_config(page_title="Color Picker from Image", page_icon="🎨", layout="wide")
st.title("🎨 Color Picker from Image")

st.markdown("""
<style>
    .header, .footer {
        visibility: hidden;
    }
    .palette {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
    }
    .color-box {
        width: 100px;
        height: 100px;
        margin: 5px;
        border: 1px solid #ccc;
    }
</style>
""", unsafe_allow_html=True)

st.write("Upload an image and get its color palette!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

def get_palette(image, n_colors=5):
    image = image.resize((100, 100))  # Resize to speed up processing
    img_array = np.array(image)
    img_array = img_array.reshape((img_array.shape[0] * img_array.shape[1], 3))

    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(img_array)

    colors = kmeans.cluster_centers_.astype(int)

    return colors

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    colors = get_palette(image)

    st.write("Palette:")
    color_boxes = ""
    for color in colors:
        color_hex = '#%02x%02x%02x' % tuple(color)
        color_boxes += f"<div class='color-box' style='background-color: {color_hex};'></div>"
        st.write(f"{color_hex}")

    st.markdown(f"<div class='palette'>{color_boxes}</div>", unsafe_allow_html=True)
