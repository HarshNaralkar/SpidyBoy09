import streamlit as st
from PIL import Image
import cv2
from rembg import remove
import numpy as np

# Function to enhance the image with smoothing and sharpening
def enhance_image(image_path):
    img = cv2.imread(image_path)
    smoothed_img = cv2.bilateralFilter(img, d=15, sigmaColor=75, sigmaSpace=75)
    blurred = cv2.GaussianBlur(smoothed_img, (21, 21), 0)
    enhanced_img = cv2.addWeighted(smoothed_img, 1.5, blurred, -0.5, 0)
    return enhanced_img

# Function to remove background and save as PNG
def remove_background(image_path):
    with open(image_path, 'rb') as input_file:
        input_image = input_file.read()
    output_image = remove(input_image)
    return output_image

# Streamlit Page Configuration
st.set_page_config(
    page_title="Image Enhancer & Background Remover",
    page_icon="🖼️",
    layout="centered"
)

# CSS for responsiveness and styling
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        color: #333;
    }
    .main {
        background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            color: white;
            font-family: Arial, sans-serif;
            background-color: #020202;
            opacity: 0.9;
            background-image:  radial-gradient(#5245f7 0.45px, transparent 0.45px), radial-gradient(#5245f7 0.45px, #020202 0.45px);
            background-size: 18px 18px;
            background-position: 0 0,9px 9px;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    .stDownloadButton>button {
        padding: 10px 20px;
        text-transform: uppercase;
        border-radius: 8px;
        font-size: 17px;
        font-weight: 500;
        color: white;
        text-shadow: none;
        background: transparent;
        cursor: pointer;
        box-shadow: transparent;
        border: 1px solid #ffffff80;
        transition: 0.5s ease;
        user-select: none;
    }

    .stDownloadButton>button:hover,
    .stDownloadButton>button:focus {
        color: #ffffff;
        background: #008cff;
        border: 1px solid #008cff;
        text-shadow: 0 0 5px #ffffff, 0 0 10px #ffffff, 0 0 20px #ffffff;
        box-shadow: 0 0 5px #008cff, 0 0 20px #008cff, 0 0 50px #008cff,
                    0 0 100px #008cff;
            }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🖼️ Image Enhancer & Background Remover")
st.markdown("### Upload an image to enhance its quality and remove its background. Works seamlessly on mobile devices!")

# File uploader
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file:
    # Display the original image
    st.image(uploaded_file, caption="Original Image", use_column_width=True)

    # Save uploaded file locally
    with open("uploaded_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Processing Message
    st.markdown("### Processing your image... Please wait!")
    col1, col2= st.columns(2)
    with col1:
        # Enhance the image
        enhanced_image = enhance_image("uploaded_image.jpg")
        enhanced_path = "enhanced_image.jpg"
        cv2.imwrite(enhanced_path, enhanced_image)

        # Display the enhanced image
        st.image(enhanced_path, caption="Enhanced Image", use_column_width=True)
    with col2:
        # Remove the background
        background_removed = remove_background(enhanced_path)
        output_path = "output_image.png"
        with open(output_path, "wb") as f:
            f.write(background_removed)

        # Display the background-removed image
        st.image(output_path, caption="Background Removed (PNG)", use_column_width=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        # Download Buttons
        with open(enhanced_path, "rb") as f:
            st.download_button(
                label="Download Enhanced Image",
                data=f,
                file_name="enhanced_image.jpg",
                mime="image/jpeg"
            )
    with col3:
        with open(output_path, "rb") as f:
            st.download_button(
                label="Download PNG Image",
                data=f,
                file_name="output_image.png",
                mime="image/png"
            )
