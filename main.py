import streamlit as st
from PIL import Image
import utils

st.set_page_config(page_title="Image Similarity Finder", layout="wide")
st.title("🔍 Find Matching Pictures")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption="Uploaded Image", width=300)

    st.markdown("### Top 5 Matching Images")
    
    # Call your similarity function
    similar_images = utils.search_similar_images(uploaded_image)
    print(similar_images)

    # Show the images in a horizontal row
    cols = st.columns(5)
    for i, img in enumerate(similar_images):
        with cols[i]:
            st.image('./data/'+img, caption=f"Match {i+1}", width=300)
