#!/usr/bin/python3

import numpy as np
import streamlit as st
import tensorflow as tf

# load_model
model = tf.keras.models.load_model("mobilenet_finetune.h5")

#preprocess function
def pre_process(img):
    img = tf.keras.preprocessing.image.load_img(img, target_size=(96, 96))
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img


# setup_webpage
st.set_page_config(
    page_title="CrapGuru",
    page_icon="random",
)
st.markdown(
    """<style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """,
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='text-align: center;'>Crap Guru 👩‍🏫</h1>", unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align: center;'>Your Personal Waste-Segregation Guru</p>",
    unsafe_allow_html=True,
)

#section one -user input
with st.container():
    st.header("Show me your waste! 🗑️")
    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "HEIC"])

    if img is not None:
        st.image(img, use_column_width=True)
        img = pre_process(img)
        pred = int(tf.round(tf.nn.sigmoid(model.predict(img))))
        if pred == 0:
            st.success("Your Waste is Bio-Degradable!", icon="🌍")
        else:
            st.success("Your Waste is Non-Biodegradable!")

#section two -about
with st.container():
    st.markdown("<h1 style='text-align: center;'>About</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center;'>India generates around 62 million tonnes of waste per annum, out of which only 12 million tonnes are treated. The percentage of waste that is treated is extremely low due to the lack of segregation of waste. Crap Guru attempts to solve this issue by striking it at it's root. It aims to take waste-segregation to every household through the power of the internet, create public-awareness and improve the threshold of waste that is treated. </p>",
        unsafe_allow_html=True,
    )
