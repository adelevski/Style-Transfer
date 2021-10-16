from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import threading

from PIL import Image
import streamlit as st
from streamlit.report_thread import get_report_ctx, add_report_ctx

import load_and_stylize as las



def threading_images(image, size, models):
    args_list = [
        ("Candy", models[0], image, size), 
        ("Udnie", models[1], image, size), 
        ("Rain Princess", models[2], image, size), 
        ("Mosaic", models[3], image, size)
    ]
    results = []
    with ThreadPoolExecutor(max_workers=None) as executor:
        ctx = get_report_ctx()
        futures = [executor.submit(stylize_image, args, ctx) for args in args_list]
        for thread in executor._threads:
            add_report_ctx(thread, ctx)
        for future in as_completed(futures):
            results.append(future.result())
    return results



def setup():
    st.title('Style Transfer Dashboard')
    st.write('Upload an image in the siderbar to the left that you would like stylized and pick an output image size.')
    st.write('Warning: Big images will take more time to be stylized!')
    st.write('Your uploaded image will be stylized in all of the following styles:')

def make_header_columns():
    c1, c2, c3, c4 = st.beta_columns(4)

    with c1:
        st.header("Candy")
        im1 = Image.open("style_images/candy.jpg")
        im1.thumbnail((256, 256), Image.ANTIALIAS)
        st.image(im1, use_column_width=False)
    with c2:
        st.header("Udnie")
        im2 = Image.open("style_images/udnie.jpg")
        im2.thumbnail((256, 256), Image.ANTIALIAS)
        st.image(im2, use_column_width=False)       
    with c3:
        st.header("Rain Princess")
        im3 = Image.open("style_images/rain_princess.jpg")
        im3.thumbnail((256, 256), Image.ANTIALIAS)
        st.image(im3, use_column_width=False)
    with c4:
        st.header("Mosaic")
        im4 = Image.open("style_images/mosaic.jpg")
        im4.thumbnail((312, 312), Image.ANTIALIAS)
        st.image(im4, use_column_width=False)


def stylize_image(args, ctx):
    add_report_ctx(threading.currentThread(), ctx)
    img = las.stylize(args[1], args[2], args[3])
    return args[0], img