"""
File contains the footer of magnet-engine.

Source: https://github.com/moetomg/magnet-engine
"""
import streamlit as st

from htbuilder.units import percent, px
from htbuilder import HtmlElement, div, br, hr, a, p, img, styles

def image(src, **style):
    """
    Create an image element.
    
    Args:
        src (string): The image source file.
        **style (dictionary): The dictionary contains CSS properties and values
    """ 
    return img(src=src, style=styles(**style))

def link(link, text, **style):
    """
    Create a hyperlink to a linked website.
    
    Args:
        link (string): The website.
        text (object): The description of the hyperlink.
        **style (dictionary): The dictionary contains CSS properties and values
    """ 
    return a(_href=link, _target="_blank", style=styles(**style))(text)
    
def footer():
    """
    Create the footer for the GUI.

    """ 
    # Create a dictionary contains the objects to be displayed
    myargs = [
        "<b>Made with</b>: Python 3.11 ",
        link("https://www.python.org/", image('https://i.imgur.com/ml09ccU.png',
        	width=px(18), height=px(18), margin= "0em")),
        ", Streamlit ",
        link("https://streamlit.io/", image('https://docs.streamlit.io/logo.svg',
        	width=px(24), height=px(25), margin= "0em")),
        ", Docker ",
        link("https://www.docker.com/", image('https://upload.wikimedia.org/wikipedia/commons/e/ea/Docker_%28container_engine%29_logo_%28cropped%29.png',
              width=px(20), height=px(18), margin= "0em")),
        " and Google APP Engine ",
        link("https://cloud.google.com/appengine", image('https://lh3.ggpht.com/_uP6bUdDOWGS6ICpMH7dBAy5LllYc_bBjjXI730L3FQ64uS1q4WltHnse7rgpKiInog2LYM1',
              width=px(19), height=px(19), margin= "0em", align="top")),
        br(),
    ]
    
    # Define the plotting styles
    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
    </style>
    """
    style_div = styles(
        left=0,
        bottom=0,
        margin=px(-50, 0, 0, 0),
        width=percent(100),
        text_align="center",
        height="60px",
        opacity=0.6
    )
    style=styles()
    st.markdown(style, unsafe_allow_html=True)

    # Define and plot the main body
    body = p()
    for arg in myargs:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)
    foot = div(style=style_div)(hr(style=styles()), body)
    st.markdown(str(foot), unsafe_allow_html=True)
