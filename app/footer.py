from streamlit.html import HtmlElement, img, a, div, p
from streamlit.html import styles
import streamlit as st

def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):
    style = """
    <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp { bottom: 60px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        right=0,
        bottom=0,
        margin=px(0, 15, 0, 0),
        text_align="center",
        opacity=0.5,
    )

    body = p()
    foot = div(
        style=style_div
    )(
        body
    )

    st.markdown(style, unsafe_allow_html=True)
    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)
    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    myargs = [
        link("https://bigganblog.org/2021/03/গতির-সমীকরণ", image('https://raw.githubusercontent.com/rafisics/suvat_calculator/main/img/bigganblog_badge_black_white.png',)),
    ]
    layout(*myargs)







def footer():
    myargs = [
        link("https://www.meiklabs.com", image('https://raw.githubusercontent.com/rafisics/suvat_calculator/main/img/bigganblog_badge_black_white.png',)),
    ]
    layout(*myargs)

if __name__ == "__main__":
    footer()
