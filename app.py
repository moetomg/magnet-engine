import altair as alt 
from os import getcwd
from os.path import join
from pandas import DataFrame

import streamlit as st
from htbuilder import HtmlElement, div, br, hr, a, p, img, styles

@st.cache_resource
def load_model(model,mdl_path,material):
    if model == "Sydney":
        from Sydney.Sydney import SydneyModel 
        mdl = SydneyModel(mdl_path,material)
    elif model == "Paderborn":
        from Paderborn.Paderborn import PaderbornModel
        mdl = PaderbornModel(mdl_path,material)
    return mdl

@st.cache_resource        
def make_donut(input_response, input_text, input_color, range=[50,450]):
    if input_color == 'blue':
        chart_color = ['#29b5e8', '#155F7A']
    if input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    if input_color == 'orange':
        chart_color = ['#F39C12', '#875A12']
    if input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']
    if input_color == 'purple':
        chart_color = ['#8f94fb', '#4e54c8']
    
    ratio = round((input_response-range[0])/(range[1]-range[0])*100)

    source = DataFrame({
        "Topic": ['', input_text],
        "% value": [100-ratio, ratio]
    })
    source_bg = DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })
        
    plot = alt.Chart(source).mark_arc(innerRadius=40, cornerRadius=22).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=128, height=128)
        
    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=30, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response}'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=40, cornerRadius=22).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=128, height=128)
    return plot_bg + plot + text

def generateTriSequence(time,amplitude, phase, duty):
    yData = []
    for i in range(len(time)): 
        if duty+phase/360 <=1:
            if time[i]<=phase/360:
                yData.append(-amplitude + (phase/360-time[i])*(2*amplitude)/(1-duty))
            elif time[i]<=phase/360+duty:
                yData.append(-amplitude + (time[i]-phase/360)*(2*amplitude)/duty)
            else:
                yData.append(amplitude - (time[i]-phase/360-duty)*(2*amplitude)/(1-duty))
            
        else:
            if (time[i]<=phase/360-(1-duty)):
                yData.append(amplitude - (phase/360-(1-duty)-time[i])*(2*amplitude)/duty)
            elif(time[i]<=phase/360):
                yData.append(amplitude - (time[i]-(phase/360-(1-duty)))*(2*amplitude)/(1-duty))
            else:
                yData.append(-amplitude + (time[i]-phase/360)*(2*amplitude)/duty)
                    
    return yData

def generateTrapSequence(time,amplitude, phase, duty1, duty2):
    yData = []
    for i in range(len(time)):
        if phase/360<=(1-duty1-duty2)/2:
            if time[i]<=phase/360:
                yData.append(-amplitude)
            elif time[i]<=phase/360+duty1:
                yData.append(-amplitude+(time[i]-phase/360)*(2*amplitude)/duty1)
            elif time[i]<=phase/360+duty1+(1-duty1-duty2)/2:
                yData.append(amplitude)
            elif time[i]<=phase/360+duty1+(1-duty1-duty2)/2+duty2:
                yData.append(amplitude-(time[i]-(phase/360+duty1+(1-duty1-duty2)/2))*(2*amplitude)/duty2) 
            else:
                yData.append(-amplitude)
             
        elif(phase/360<=(1-duty1-duty2)/2+duty2):
            if (time[i]<=phase/360-((1-duty1-duty2)/2)): 
                yData.append(-amplitude+((phase/360-(1-duty1-duty2)/2)-time[i])*(2*amplitude)/duty2) 
            elif (time[i]<=phase/360):
                yData.append(-amplitude) 
            elif (time[i]<=phase/360+duty1):
                yData.append(-amplitude+(time[i]-phase/360)*(2*amplitude)/duty1) 
            elif (time[i]<=phase/360+duty1+(1-duty1-duty2)/2):
                yData.append(amplitude) 
            else:
                yData.append(amplitude-(time[i]-(phase/360+duty1+(1-duty1-duty2)/2))*(2*amplitude)/duty2)
            
        elif (phase/360<=(1-duty1-duty2)+duty2):
            if (time[i]<=phase/360-(1-duty1-duty2)/2-duty2):
                yData.append(amplitude)
            elif (time[i]<=phase/360-(1-duty1-duty2)/2):
                yData.append(amplitude-(time[i]-(phase/360-(1-duty1-duty2)/2-duty2))*(2*amplitude)/duty2)
            elif (time[i]<=phase/360):
                yData.append(-amplitude)
            elif (time[i]<=phase/360+duty1):
                yData.append(-amplitude+(time[i]-phase/360)*(2*amplitude)/duty1)
            else:
                yData.append(amplitude)
            
        else:
            if (time[i]<=phase/360-(1-duty1-duty2)-duty2):
                yData.append(amplitude-((phase/360-(1-duty1-duty2)-duty2)-time[i])*(2*amplitude)/duty1)
            elif (time[i]<=phase/360-(1-duty1-duty2)/2-duty2):
                yData.append(amplitude)
            elif (time[i]<=phase/360-(1-duty1-duty2)/2):
                yData.append(amplitude-(time[i]-(phase/360-(1-duty1-duty2)/2-duty2))*(2*amplitude)/duty2)
            elif (time[i]<=phase/360):
                yData.append(-amplitude)
            else:
                yData.append(-amplitude+(time[i]-phase/360)*(2*amplitude)/duty1)
    return yData       
        
# ----------------------------------------------------------------------- footer 
def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)
    
@st.cache_data
def footer():
    from htbuilder.units import percent, px

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
    style_hr = styles(
    )
    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)
    st.markdown(style, unsafe_allow_html=True)

    for arg in myargs:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def main():
    # ------------------------------------------------------------------- Page configuration 
    # Set logo and name 

    st.set_page_config(
        page_title="MagNet Engine",
        page_icon="🧲",
        layout="wide",
        initial_sidebar_state="expanded")

    directory = getcwd()
    icon_folder = join(directory, "icons")
    # ------------------------------------------------------------------- Parameters init
    
    models = ['Paderborn','Sydney']
    materials = ['3C90','3C92','3C94','3C95','3E6' ,
                 '3F4' ,'77'  ,'78'  ,'79'  ,'ML95S',
                 'N27' ,'N30' ,'N49' ,'N87' ,'T37']
    resolution_params = {
                "Sydney": 128,
                "Paderborn": 1024,    
            } # Model resolution 
    
    if 'shape_id' not in st.session_state:
        st.session_state['shape_id'] = 0 # 0-sin 1-tri 2-trap 3-user
   
    shapes = [
        ('Sinusoidal ∿', 'sine.svg'),
        ('Triangular △', 'tri.svg'),
        ('Trapzoidal ☖', 'trap.svg'),
        ('Customize  ✐', 'user.svg')
        ]

    # Waveform parameters
    if 'amplitude' not in st.session_state:
        st.session_state['amplitude'] = 100
    if 'duty' not in st.session_state:
        st.session_state['duty'] = 0.4
    if 'duty2' not in st.session_state:
        st.session_state['duty2'] = 0.3
    if 'phase' not in st.session_state:
        st.session_state['phase'] = 0

    # ------------------------------------------------------------------- Side bar     
    # set body margin
    with st.sidebar:
        st.write("""
        <div style='position: relative; top: -30px; margin-bottom: -30px;'>
            <span style='font-size: calc(0.8vw + 0.8vh + 10px); text-decoration: none; font-weight: bold; text-align: left;'>
                🧲 MagNet Engine
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Model and material selector 
        model = st.selectbox('Select a model', models, index=len(models)-1)
        folder = join(directory, model, "models")
        material = st.selectbox('Target material', materials, index=len(materials)-1)
        mdl_path = folder+"/"+material+".pt"
        # Initialize the model 
        mdl = load_model(model,mdl_path,material)

        # Seperator
        st.sidebar.markdown(
            """
            <div style='margin-top: 10px; margin-bottom: 10px; height:5px;
                    border:none;
                    color:#808080;
                    background-color:#808080;'>
            </div>
            """, 
            unsafe_allow_html=True)
        
        st.sidebar.title("MagNet tools")
        st.markdown(
        """
        <style>
            .styled-link a {
                text-decoration: none; 
                color: rgb(199, 235, 223); 
            }
            
            .styled-link a:hover {
                color: rgba(41, 121, 255, 1); 
            }
        </style>
        
        <div class="styled-link" style='background-color: rgba(42, 62, 87, 1); padding: 20px; border-radius: 10px;'>
            Data information: <a href="https://www.princeton.edu/~minjie/magnet.html">MagNet  Database</a><br>
            AI platform: <a href="https://mag-net.princeton.edu/">MagNet-AI Platform</a><br>
            Github repo: <a href="https://github.com/upb-lea/mag-net-hub">MagNet Toolkit</a><br>
            
        </div>
        """, unsafe_allow_html=True
        )
        
        st.sidebar.title("Support")
        st.sidebar.info(
        """
        Issues with app usage, please contact: 
        sinan.li@sydney.edu.au
        """
        )
        st.sidebar.markdown(
            """
            <div style='margin-top: 10px; margin-bottom: 10px; height:0px;
                    border:none;
                    color:transparent;
                    background-color:transparent;'>
            </div>
            """, 
            unsafe_allow_html=True)
        
        st.image("https://openday.sydney.edu.au/static/website/images/usyd-logo-white.png",caption="Powered by: Sydney University",use_column_width=True)

    # ------------------------------------------------------------------- main body  

    # set body margin 
    margins_css = """
        <style>
            .main > div {
                padding-left: 2rem;
                padding-right: 1rem;
                padding-top: 1.8rem;
                padding-bottom: -1rem;
            }

            [data-testid="column"]  [data-testid="stHorizontalBlock"]  [data-testid="column"]{
                min-width: 1px !important;
            }
        </style>
    """
    st.markdown(margins_css, unsafe_allow_html=True)

    # Define the layout 
    col1, _, col2, _, col3 ,_ = st.columns([1.2,0.05,1.3,0.1,1.2,0.05])  # First row
    st.markdown("<div style='height:0.5vh;'></div>", unsafe_allow_html=True)
    col4, _, col5, _, col6 ,_ = st.columns([1.2,0.05,1.3,0.1,1.2,0.05])  # Second row

    # Setting themes
    alt.themes.enable("dark")
    
    # First row 
    with col1:
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none;font-weight: bold;text-align: left;'> Excitation Waveform [B] </span>""",unsafe_allow_html=True)

        # ************************* Shape selector 
        _, col1_1, col1_2 = st.columns([0.15,1,1]) 
        for i, (label, icon_filename) in enumerate(shapes):
            with col1_1 if (i==0 or i==2) else col1_2:
                icon_path = join(icon_folder, icon_filename)
                with open(icon_path, "r") as file:
                    svg_code = file.read()    
                if st.button(label):
                    st.session_state['shape_id'] = i
                st.write(f'<div style="text-align: left; margin-left:calc(40px - 1.5vw);"><span style="display: inline-block; width: calc(4vw + 25px); height: calc(4vh + 60px); fill: #F5F5F5;">{svg_code}</span></div>', unsafe_allow_html=True)

    with col3:
        import streamlit_vertical_slider as svs

        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none;font-weight: bold;text-align: left;'> Excitation Parameters [B]</span>""",unsafe_allow_html=True)

        # ************************ Waveform parameters setting
        # layout setting 
        if st.session_state['shape_id'] == 0:
            col3_1, col3_2 = st.columns([1, 1]) 
        elif st.session_state['shape_id'] == 1:
            col3_1, col3_2, col3_3 = st.columns([1, 1, 1]) 
        elif st.session_state['shape_id'] == 2:
            col3_1, col3_2, col3_3, col3_4 = st.columns([1, 1, 1, 1])           
  
        # slider setting
        if st.session_state['shape_id'] != 3: 
            with col3_1:  
                st.session_state['amplitude'] = svs.vertical_slider(
                            label="Bac [mT]",
                            key="slider1", 
                            default_value=100, 
                            step=1, 
                            min_value=10, 
                            max_value=300,
                            track_color = "blue", #Optional - Defaults to Streamlit Red
                            slider_color = ("#4A00E0","#8E2DE2"), #Optional
                            thumb_color= "#FC5C7D", #Optional - Defaults to Streamlit Red
                            thumb_shape = "pill",
                            value_always_visible = True ,#Optional - Defaults to False
                            height=241,
                            )
            with col3_2:
                    st.session_state['phase'] = svs.vertical_slider(
                                label="φᵢ [°]",
                                key="slider2", 
                                default_value=0, 
                                step=1, 
                                min_value=0, 
                                max_value=360,
                                track_color = "blue", #Optional - Defaults to Streamlit Red
                                slider_color = ("#4A00E0","#8E2DE2"), #Optional
                                thumb_color= "#FC5C7D", #Optional - Defaults to Streamlit Red
                                value_always_visible = True ,#Optional - Defaults to False
                                thumb_shape = "pill",
                                height=239,
                                )
        if st.session_state['shape_id'] == 1 or st.session_state['shape_id'] == 2: 
            with col3_3:
                if st.session_state['shape_id'] == 1:
                    st.session_state['duty'] = svs.vertical_slider(
                        label="duty cycle [%]",
                        key="slider3", 
                        default_value=40, 
                        step=1, 
                        min_value=1, 
                        max_value=100,
                        track_color = "blue", #Optional - Defaults to Streamlit Red
                        slider_color = ("#4A00E0","#8E2DE2"), #Optional
                        thumb_color= "#FC5C7D", #Optional - Defaults to Streamlit Red
                        value_always_visible = True ,#Optional - Defaults to False
                        thumb_shape = "pill",
                        height=241,
                        )/100
                else: 
                    st.session_state['duty'] = svs.vertical_slider(
                        label="rising duty [%]",
                        key="slider4", 
                        default_value=40, 
                        step=1, 
                        min_value=1, 
                        max_value=99,
                        track_color = "blue", #Optional - Defaults to Streamlit Red
                        slider_color = ("#4A00E0","#8E2DE2"), #Optional
                        thumb_color= "#FC5C7D", #Optional - Defaults to Streamlit Red
                        value_always_visible = True ,#Optional - Defaults to False
                        thumb_shape = "pill",
                        height=241,
                        )/100
        if  st.session_state['shape_id'] == 2:  
            with col3_4:
                st.session_state['duty2'] = svs.vertical_slider(
                    label="falling duty [%]",
                    key="slider5", 
                    default_value=(100-st.session_state['duty']*100)/2, 
                    step=1, 
                    min_value=1, 
                    max_value=100-st.session_state['duty']*100,
                    track_color = "blue", #Optional - Defaults to Streamlit Red
                    slider_color = ("#4A00E0","#8E2DE2"), #Optional
                    thumb_color= "#FC5C7D", #Optional - Defaults to Streamlit Red
                    value_always_visible = True ,#Optional - Defaults to False
                    thumb_shape = "pill",
                    height=241,
                    )/100
                
        if st.session_state['shape_id'] == 3: 
            uploaded_file = st.file_uploader("Resolution >= :red["+str(resolution_params[model])+" steps]", type=['csv'], help="Load user-defined flux excitation and :red[only read data in the 1st row].")

    with col4:
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none;font-weight: bold;text-align: left;'> Operating Condition [f, T]</span><div style='margin-bottom: 3vh;'></div>""",unsafe_allow_html=True)

        # ************************ Frequency/Temperature setting
        #_,col4_1, _, col4_2, _ = st.columns([0.3, 1, 0.1, 1.5, 0.1])
        _, col4_1, _, col4_2 = st.columns([0.18,1.1,0.12,1.2])
        with col4_1:
            st.markdown("<div ></div>", unsafe_allow_html=True)
            Frequency = st.number_input("Frequency, f [kHz]", format="%d", value=100, step=1,min_value=10,max_value=450)
            st.markdown("<div style='height:3vw;'></div>", unsafe_allow_html=True)
            Temperature = st.number_input("Temperature, T [°C]", format="%d", value=25, step=1,min_value=25,max_value=90)
        
        with col4_2:
            donut_chart_F = make_donut(Frequency, 'Frequency', 'blue', [10,450])
            st.altair_chart(donut_chart_F, use_container_width=True)
            donut_chart_T = make_donut(Temperature, 'Temperature', 'red', [25,90])
            st.altair_chart(donut_chart_T, use_container_width=True)

    with col2:
        from numpy import array, linspace, genfromtxt, arange, append, sin, pi
        
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none;font-weight: bold;text-align: left;'> Time-Domain Response [B-H]</span>""",unsafe_allow_html=True)

        #************************* Draw waveform 
        # Data loading 
        t = linspace(0, 0, resolution_params[model])
        B = linspace(0, 0, resolution_params[model])
        if st.session_state['shape_id'] == 0: 
            t = linspace(0, 1, resolution_params[model])
            B = st.session_state['amplitude']*sin((360*t+st.session_state['phase'])*pi/180)
        elif st.session_state['shape_id'] == 1:
            t = linspace(0, 1, resolution_params[model])
            B = array(generateTriSequence(t,st.session_state['amplitude'], st.session_state['phase'], st.session_state['duty']))
        elif st.session_state['shape_id'] == 2:  
            t = linspace(0, 1, resolution_params[model])  
            B = array(generateTrapSequence(t,st.session_state['amplitude'], st.session_state['phase'], st.session_state['duty'], st.session_state['duty2']))
        else: 
            if uploaded_file is not None: 
                t = linspace(0, 1, resolution_params[model])  
                first_row = genfromtxt(uploaded_file, delimiter=',', max_rows=1)
                index = [int(x) for x in arange(0, len(first_row)-1, (len(first_row)-1)/ resolution_params[model])]
                B = array(first_row[index].tolist())*1000  # convert to mT
       
        # Predict H and Pv 
        
        if sum(B) == 0:
            H  = linspace(0, 0, resolution_params[model])
        else:
            P ,H = mdl(B/1000,Frequency*1000,Temperature) # convert to B in [T], f in [Hz]
            H = H.squeeze()

        # Plot setting  
        df = DataFrame(columns=['t', 'B','H'])
        df['t'] = t
        df['B'] = B
        df['H'] = H
        base = alt.Chart(df.reset_index()).encode(x=alt.X('t',title='Fraction of a Cycle', axis=alt.Axis(titlePadding=14,titleFontWeight='bold')))
        chart = alt.layer(
            base.mark_line(strokeWidth=5,stroke='#8E2DE2').encode(y=alt.X('B',title='B [mT]', axis=alt.Axis(titlePadding=0,titleFontWeight='bold',grid=True, titleColor='#8E2DE2'))),
            base.mark_line(strokeWidth=5,stroke='#E74C3C').encode(y=alt.X('H',title='H [A/m]', axis=alt.Axis(titlePadding=10,titleFontWeight='bold',grid=True, gridDash=[3, 3], titleColor='#E74C3C')))
        ).resolve_scale(y='independent')

        chart = chart.configure_axis(grid=True)
        chart = chart.properties(height=330)
        st.altair_chart(chart, use_container_width=True)
        
    with col5:
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none;font-weight: bold;text-align: left;'> Steady-State Loop [B-H]</span>""",unsafe_allow_html=True)

        df2 = DataFrame(columns=['B','H'])
        df2['B'] = append(B, B[0])
        df2['H'] = append(H, H[0])
        chart2 = alt.Chart(df2).mark_line(strokeWidth=5,stroke='#29b5e8').encode(
            x=alt.X('H',title='H [A/m]', axis=alt.Axis(titlePadding=5,titleFontWeight='bold',grid=True), sort=None,scale=alt.Scale(domain=(round(min(H)-0.05*(max(H)-min(H))), round(max(H)+0.05*(max(H)-min(H)))))),
            y=alt.Y('B',title='B [mT]', axis=alt.Axis(titlePadding=0,titleFontWeight='bold',grid=True)), 
        ).properties(height=330)
        st.altair_chart(chart2, use_container_width=True)
        
    with col6:
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none;font-weight: bold;text-align: left;'> Volumetric Loss [Pv]</span>""",unsafe_allow_html=True)

        # ------------------------------------------------------ Show Pv
        custom_css = """
        .metric-container {
            background-color: #875A12; 
            border-radius: 10px;  
            padding: 0px; 
        }
        .metric-container h1 {
            font-size: calc(2vw + 2vh + 10px); 
            color: #f38612;  
            text-align: center;
            padding-top: calc(1vw + 1vh);  
            padding-bottom: 0px;    
        }
        .metric-container p {
            font-size: calc(0.5vw + 0.5vh + 5px); 
            color: white;  
            text-align: center;
            padding-bottom: 1.2vw; 
        }
        """
        st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
        
        # Show customize metric container
        if sum(B) == 0:
            st.markdown(f'<div class="metric-container"><h1>Unknown</h1><p>kW/m³</p></div>', unsafe_allow_html=True)   
            
            # Add gaps  
            st.markdown("<div style='height:2vh;'></div>", unsafe_allow_html=True)
            _, col6_1 = st.columns([1.4,1])
            with col6_1:
                # Disabled download button
                text_contents = '''Error occurs during downloading'''
                st.download_button("Download\n\n 📂", text_contents, disabled=True)
        else: 
            st.markdown(f'<div class="metric-container"><h1>{round(P/1000,2)}</h1><p>kW/m³</p></div>', unsafe_allow_html=True)
            
            # Add gaps  
            st.markdown("<div style='height:2vh;'></div>", unsafe_allow_html=True)
            _, col6_1 = st.columns([1.4,1])
            with col6_1:
                # Create the csv file to B, H, Pv 
                df3 = DataFrame(columns=['B [mT]','H [A/m]','Pv [W/m3]'])
                df3['B [mT]'] = B
                df3['H [A/m]'] = H
                df3['Pv [W/m3]'] = [P] + [None] * (len(B) - 1)
                csv = df3.to_csv()
                st.download_button(
                    #label=":orange[Download]\n\n :orange[B-H Results]",
                    label="Download 📂",
                    help="Download B-H-Pv in "+str(resolution_params[model])+ " step as CSV",
                    data=csv.encode('utf-8'),
                    file_name='magnet-engine_prediction.csv',
                    use_container_width = True,
                    mime='text/csv',
                )


if __name__ == "__main__":
    main()
    footer()

