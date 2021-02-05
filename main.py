import streamlit as st
from PIL import Image
import load_and_stylize as las

st.set_page_config(layout="wide")

candy = las.load_model("saved_models/candy.pth")
mosaic = las.load_model("saved_models/mosaic.pth")
rain = las.load_model("saved_models/rain_princess.pth")
udnie = las.load_model("saved_models/udnie.pth")

st.title('Style Transfer Dashboard')

st.write('Upload an image in the siderbar to the left that you would like stylized and download your favorite style! (or all of them ;) hehehe)')

st.write('Warning: Big images will take more time to be stylized!')

st.write('Currently, we have four styles to choose from:')

c1, c2, c3, c4 = st.beta_columns(4)

with c1:
    st.header("Candy")
    im1 = Image.open("style_images/candy.jpg")
    st.image(im1, use_column_width=True)
with c2:
    st.header("Mosaic")
    im2 = Image.open("style_images/mosaic.jpg")
    st.image(im2, use_column_width=True)
with c3:
    st.header("Rain Princess")
    im3 = Image.open("style_images/rain_princess.jpg")
    st.image(im3, use_column_width=True)
with c4:
    st.header("Udnie")
    im4 = Image.open("style_images/udnie.jpg")
    st.image(im4, use_column_width=True)

uploaded_file = st.sidebar.file_uploader("Choose an image...")
if uploaded_file is not None:
    try:
        image = uploaded_file.read()
        st.sidebar.image(image, caption='Uploaded Image.', use_column_width=True, width=400)

        st.header("Candy")
        img = las.stylize(candy, image)
        st.image(img, column_width=200)


        st.header("Mosaic")
        img = las.stylize(mosaic, image)
        st.image(img, column_width=200)


        st.header("Rain Princess")
        img = las.stylize(rain, image)
        st.image(img, column_width=200)


        st.header("Udnie")
        img = las.stylize(udnie, image)
        st.image(img, column_width=200)

    except:
        st.write("Invalid Image!")

