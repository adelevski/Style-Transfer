from PIL import Image
import streamlit as st
from streamlit.report_thread import add_report_ctx

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import funcs
import load_and_stylize as las


def threading_images(func, values):
    results = []
    with ThreadPoolExecutor(max_workers=None) as executor:
        ctx = st.report_thread.add_report_ctx()
        futures = [executor.submit(func, args, ctx) for args in values]
        for future in as_completed(futures):
            results.append(future.result())
    return results

st.set_page_config(layout="wide")

candy = las.load_model("saved_models/candy.pth")
mosaic = las.load_model("saved_models/mosaic.pth")
rain = las.load_model("saved_models/rain_princess.pth")
udnie = las.load_model("saved_models/udnie.pth")

funcs.setup()
funcs.make_header_columns()

uploaded_file = st.sidebar.file_uploader("Choose an image...")
if uploaded_file:
    image = uploaded_file.read()
    st.sidebar.image(image, caption='Uploaded Image.', use_column_width=False, width=200)

    image_size = st.sidebar.selectbox(
        label = "Output image size? (The bigger the image the slower the transfer will be)",
        options = ("Output image size...", "128x128", "256x256", "512x512", "1024x1024"),
        index = 0
    )
    if image_size != "Output image size...":
        size = int(image_size.split('x')[0])

        arguments_list = [
            ("Candy", candy, image, size), 
            ("Mosaic", mosaic, image, size), 
            ("Rain Princess", rain, image, size), 
            ("Udnie", udnie, image, size)
        ]
        results = threading_images(funcs.stylize_image, arguments_list)

        try:
            # print(results)
            for name, img in results:
                st.header(name)
                st.image(img, column_width=100)

        except Exception as e:
            st.write("Invalid Image!")
            st.write(e)
