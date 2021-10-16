from PIL import Image
import streamlit as st

import load_and_stylize as las


def setup():
    st.title('Style Transfer Dashboard')
    st.write('Upload an image in the siderbar to the left that you would like stylized and download your favorite style! (or all of them ;) hehehe)')
    st.write('Warning: Big images will take more time to be stylized!')
    st.write('Currently, we have four styles to choose from:')

def make_header_columns():
    c1, c2, c3, c4 = st.beta_columns(4)

    with c1:
        st.header("Candy")
        im1 = Image.open("style_images/candy.jpg")
        im1.thumbnail((256, 256), Image.ANTIALIAS)
        st.image(im1, use_column_width=False)
    with c2:
        st.header("Mosaic")
        im2 = Image.open("style_images/mosaic.jpg")
        im2.thumbnail((256, 256), Image.ANTIALIAS)
        st.image(im2, use_column_width=False)
    with c3:
        st.header("Rain Princess")
        im3 = Image.open("style_images/rain_princess.jpg")
        im3.thumbnail((256, 256), Image.ANTIALIAS)
        st.image(im3, use_column_width=False)
    with c4:
        st.header("Udnie")
        im4 = Image.open("style_images/udnie.jpg")
        im4.thumbnail((256, 256), Image.ANTIALIAS)
        st.image(im4, use_column_width=False)


def stylize_image(args, ctx):
    img = las.stylize(args[1], args[2], args[3])
    return args[0], img