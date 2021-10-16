from PIL import Image
import streamlit as st

import funcs
import load_and_stylize as las


st.set_page_config(layout="wide")

candy = las.load_model("saved_models/candy.pth")
rain = las.load_model("saved_models/rain_princess.pth")
udnie = las.load_model("saved_models/udnie.pth")
mosaic = las.load_model("saved_models/mosaic.pth")

models = [candy, udnie, rain, mosaic]

funcs.setup()
funcs.make_header_columns()

uploaded_file = st.sidebar.file_uploader("Choose an image...")
if uploaded_file:
    image = uploaded_file.read()
    st.sidebar.image(image, caption='Uploaded Image.', use_column_width=False, width=200)

    image_size = st.sidebar.selectbox(
        label = "Choose output image size:",
        options = ("None", "128x128", "256x256", "512x512", "1024x1024"),
        index = 0
    )
    if image_size != "None":
        size = int(image_size.split('x')[0])
        results = funcs.threading_images(image, size, models)
        try:
            # print(results)
            for name, img in results:
                st.header(name)
                st.image(img, column_width=100)

        except Exception as e:
            st.write("Invalid Image!")
            st.write(e)
