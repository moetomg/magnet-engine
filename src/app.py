"""
File contains the magnet-engine web-based GUI, powered by streamlit.

Source: https://github.com/moetomg/magnet-engine
"""
import streamlit as st
import streamlit_vertical_slider as svs

from os import getcwd
from os.path import join
from pandas import DataFrame
from footer import footer
from utils import load_model, draw_donut, draw_line, generateTriSequence, generateTrapSequence

def main():
    """
    GUI main page setting.
    
    """
    # Page logo and size configuration 
    st.set_page_config(
        page_title = "MagNet Engine",
        page_icon = "🧲",
        layout = "wide",
        initial_sidebar_state = "expanded")

    # Extract icon folder address
    directory = getcwd()
    icon_folder = join(directory, "icons")
    
    # Define model and material choices
    models = ['Paderborn','Sydney']
    resolution_params = {
                "Sydney": 128,
                "Paderborn": 1024,    
            } # Model resolution 
    materials = ['3C90','3C92','3C94','3C95','3E6' ,
                '3F4' ,'77'  ,'78'  ,'79'  ,'ML95S',
                'N27' ,'N30' ,'N49' ,'N87' ,'T37']
    # Define user waveform choice 
    if 'shape_id' not in st.session_state:
        st.session_state['shape_id'] = 0 # 0-sin 1-tri 2-trap 3-user
    
    # Define waveform selection icon
    shapes = [
        ('Sinusoidal ∿', 'sine.svg'),
        ('Triangular △', 'tri.svg'),
        ('Trapezoidal ☖', 'trap.svg'),
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

    # Define the side bar 
    with st.sidebar:
        # Sidebar style setting 
        st.write("""
        <div style='position: relative; top: -30px; margin-bottom: -30px;'>
            <span style='font-size: calc(0.8vw + 0.8vh + 10px); text-decoration: none; font-weight: bold; text-align: left;'>
                🧲 MagNet Engine
            </span>
        </div>
        """, unsafe_allow_html=True)

        # Model and material selector 
        model = st.selectbox('Select a model', models, index=len(models)-1)
        material = st.selectbox('Target material', materials, index=len(materials)-1)
        
        # Initialize and load the model 
        mdl = load_model(model,material)

        # White space acts as separator
        st.sidebar.markdown(
            """
            <div style='margin-top: 10px; margin-bottom: 10px; height:5px;
                    border: none;
                    color: #808080;
                    background-color: #808080;'>
            </div>
            """, 
            unsafe_allow_html=True)

        # Display message
        st.write("""<div style='margin-top: 2px; margin-bottom: 15px;'><span style='font-size: calc(0.7vw + 10px); text-decoration: none; font-weight: bold; text-align: left; font-family: sans-serif;'> MagNet tools</span></div>""", unsafe_allow_html=True)
        
        # Set text box style
        st.markdown(
        """
        <style>
            .styled-link{
                font-size: 17px;
            }
            .styled-link a {
                text-decoration: none; 
                color: rgb(199, 235, 223); 
                font-size: 17px;
            }
            .styled-link a:hover {
                color: rgba(41, 121, 255, 1); 
            }
        </style>
        
        <div class="styled-link" style='background-color: rgba(42, 62, 87, 1); padding: 15px; border-radius: 10px;'>
            Data information: <a href="https://www.princeton.edu/~minjie/magnet.html">MagNet  Database</a><br>
            AI platform: <a href="https://mag-net.princeton.edu/">MagNet-AI Platform</a><br>
            Github repo: <a href="https://github.com/upb-lea/mag-net-hub">MagNet Toolkit</a><br>
        </div>
        """, unsafe_allow_html=True)
        
        # Display message
        st.write("""<div style='margin-top: 10px; margin-bottom: 5px;'> <span style='font-size: calc(0.7vw + 10px); text-decoration: none; font-weight: bold; text-align: left; font-family: sans-serif;'> Contact us</span></div>""", unsafe_allow_html=True)
        st.markdown(
        """
        <div class="styled-link" style='background-color: rgba(42, 62, 87, 1); padding: 15px; border-radius: 10px; margin-top: 10px;'>
            Sinan: 
            <a href="mailto:sinan.li@sydney.edu.au">sinan.li@sydney.edu.au</a><br>
            Qiujie: 
            <a href="mailto:qiujie.huang@sydney.edu.au">qiujie.huang@sydney.edu.au</a>
        </div>
        """, unsafe_allow_html=True)
                
        # White space acts as separator
        st.sidebar.markdown(
            """
            <div style='margin-top: 10px; margin-bottom: 30px; height:0px;
                    border:none;
                    color:transparent;
                    background-color:transparent;'>
            </div>
            """, 
            unsafe_allow_html=True)
        
        # Display uni logo
        st.image("https://openday.sydney.edu.au/static/website/images/usyd-logo-white.png", caption="Powered by: Sydney University", use_column_width=True)

    # Main body style setting
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

    # Define the layout and page segmentation
    col1, _, col2, _, col3 ,_ = st.columns([1.2, 0.05, 1.3, 0.1, 1.2, 0.05])  # First row
    st.markdown("<div style='height:0.5vh;'></div>", unsafe_allow_html=True)
    col4, _, col5, _, col6 ,_ = st.columns([1.2, 0.05, 1.3, 0.1, 1.2, 0.05])  # Second row

    # Define the first element in the first row 
    with col1:
        # Display message
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none; font-weight: bold; text-align: left;'> Excitation Waveform [B] </span>""", unsafe_allow_html=True)

        # Shape selector 
        _, col1_1, col1_2 = st.columns([0.15, 1, 1]) 
        for i, (label, icon_filename) in enumerate(shapes):
            with col1_1 if (i==0 or i==2) else col1_2:
                icon_path = join(icon_folder, icon_filename)
                with open(icon_path, "r") as file:
                    svg_code = file.read()    
                if st.button(label):
                    st.session_state['shape_id'] = i
                st.write(f'<div style="text-align: left; margin-left:calc(40px - 1.5vw);"><span style="display: inline-block; width: calc(4vw + 25px); height: calc(4vh + 60px); fill: #F5F5F5;">{svg_code}</span></div>', unsafe_allow_html=True)
   
    # Define the third element in the first row 
    with col3:
        # Display message
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none;font-weight: bold;text-align: left;'> Excitation Parameters [B]</span>""", unsafe_allow_html=True)

        # Waveform parameters setting
        if st.session_state['shape_id'] == 0:
            col3_1, _, col3_2, _ = st.columns([1, 1, 1, 1]) 
        elif st.session_state['shape_id'] == 1:
            col3_1, col3_2, col3_3, _ = st.columns([1, 1, 1, 1]) 
        elif st.session_state['shape_id'] == 2:
            col3_1, col3_2, col3_3, col3_4 = st.columns([1, 1, 1, 1])           
  
        # Slider display setting
        if st.session_state['shape_id'] != 3: 
            with col3_1:  
                st.session_state['amplitude'] = svs.vertical_slider(
                            label = "Bac [mT]",
                            key = "slider1", 
                            default_value = 100, 
                            step = 1, 
                            min_value = 10, 
                            max_value = 300,
                            track_color = "blue", 
                            slider_color = ("#4A00E0", "#8E2DE2"), 
                            thumb_color = "#FC5C7D", 
                            thumb_shape = "pill",
                            value_always_visible = True,
                            height = 241)
            with col3_2:
                    st.session_state['phase'] = svs.vertical_slider(
                                label = "φᵢ [°]",
                                key = "slider2", 
                                default_value = 0, 
                                step = 1, 
                                min_value = 0, 
                                max_value = 360,
                                track_color = "blue", 
                                slider_color = ("#4A00E0", "#8E2DE2"), 
                                thumb_color = "#FC5C7D", 
                                value_always_visible = True,
                                thumb_shape = "pill",
                                height = 239)
    
        if st.session_state['shape_id'] == 1 or st.session_state['shape_id'] == 2: 
            with col3_3:
                if st.session_state['shape_id'] == 1:
                    st.session_state['duty'] = svs.vertical_slider(
                        label = "duty cycle [%]",
                        key = "slider3", 
                        default_value = 40, 
                        step = 1, 
                        min_value = 1, 
                        max_value = 100,
                        track_color = "blue", 
                        slider_color = ("#4A00E0", "#8E2DE2"),
                        thumb_color= "#FC5C7D", 
                        value_always_visible = True,
                        thumb_shape = "pill",
                        height = 241) / 100
                else: 
                    st.session_state['duty'] = svs.vertical_slider(
                        label="rising duty [%]",
                        key="slider4", 
                        default_value = 40, 
                        step = 1, 
                        min_value = 1, 
                        max_value = 99,
                        track_color = "blue", 
                        slider_color = ("#4A00E0", "#8E2DE2"), 
                        thumb_color = "#FC5C7D",  
                        value_always_visible = True,
                        thumb_shape = "pill",
                        height = 241) / 100
                    
        if  st.session_state['shape_id'] == 2:  
            with col3_4:
                st.session_state['duty2'] = svs.vertical_slider(
                    label = "falling duty [%]",
                    key = "slider5", 
                    default_value=(100 - st.session_state['duty'] * 100) / 2, 
                    step = 1, 
                    min_value = 1, 
                    max_value = 100 - st.session_state['duty'] * 100,
                    track_color = "blue", 
                    slider_color = ("#4A00E0","#8E2DE2"), 
                    thumb_color = "#FC5C7D", 
                    value_always_visible = True,
                    thumb_shape = "pill",
                    height = 241) / 100
                
        # Allow user to upload a customized waveform
        if st.session_state['shape_id'] == 3: 
            uploaded_file = st.file_uploader("Resolution >= :red["+str(resolution_params[model])+" steps]", type=['csv'], help="Load user-defined flux excitation and :red[only read data in the 1st row].")

    # Define the first element in the second row 
    with col4:
        # Display message
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none;font-weight: bold;text-align: left;'> Operating Conditions [f, T]</span><div style='margin-bottom: 3vh;'></div>""",unsafe_allow_html=True)

        # Element layout setting
        _, col4_1, _, col4_2 = st.columns([0.18, 1.1, 0.12, 1.2])
        
        # Frequency and Temperature selector setting
        with col4_1:
            # Add blank space
            st.markdown("<div ></div>", unsafe_allow_html=True)
            
            # Add slider for frequency 
            Frequency = st.number_input("Frequency, f [kHz]", format="%d", value=100, step=1, min_value=10, max_value=450)
            
            # Add blank space
            st.markdown("<div style='height:3vw;'></div>", unsafe_allow_html=True)
            
            # Add slider for temperature
            Temperature = st.number_input("Temperature, T [°C]", format="%d", value=25, step=1, min_value=25, max_value=90)
        
        with col4_2:
            # Add donut plot for frequency 
            donut_chart_F = draw_donut(Frequency, 'Frequency', 'blue', [10, 450])
            st.altair_chart(donut_chart_F, use_container_width=True)
            
            # Add donut plot for temperature
            donut_chart_T = draw_donut(Temperature, 'Temperature', 'red', [25, 90])
            st.altair_chart(donut_chart_T, use_container_width=True)

    # Define the second element in the first row 
    with col2:
        # Import numpy package
        from numpy import array, linspace, genfromtxt, arange, append, sin, pi
        
        # Display message
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none; font-weight: bold;text-align: left;'> Time-Domain Response [B-H]</span>""", unsafe_allow_html=True)

        # Data loading 
        t = linspace(0, 0, resolution_params[model])
        B = linspace(0, 0, resolution_params[model])
        if st.session_state['shape_id'] == 0: 
            t = linspace(0, 1, resolution_params[model])
            B = st.session_state['amplitude'] * sin((360 * t+st.session_state['phase']) * pi / 180)
        elif st.session_state['shape_id'] == 1:
            t = linspace(0, 1, resolution_params[model])
            B = array(generateTriSequence(t, st.session_state['amplitude'], st.session_state['phase'], st.session_state['duty']))
        elif st.session_state['shape_id'] == 2:  
            t = linspace(0, 1, resolution_params[model])  
            B = array(generateTrapSequence(t, st.session_state['amplitude'], st.session_state['phase'], st.session_state['duty'], st.session_state['duty2']))
        else: 
            if uploaded_file is not None: 
                t = linspace(0, 1, resolution_params[model])  
                first_row = genfromtxt(uploaded_file, delimiter=',', max_rows=1)
                index = [int(x) for x in arange(0, len(first_row) - 1, (len(first_row) - 1)/ resolution_params[model])]
                B = array(first_row[index].tolist()) * 1000  # convert to mT
       
        # Predict field strength and core loss density 
        if sum(B) == 0:
            H  = linspace(0, 0, resolution_params[model])
        else:
            P ,H = mdl(B / 1000, Frequency * 1000, Temperature) # convert to B in [T], f in [Hz]
            H = H.squeeze()

        # Add repeated first point to close curve
        t = append(t, t[0])
        B = append(B, B[0])
        H = append(H, H[0])
        
        # Plot setting  
        chart = draw_line(B, H, t)
        st.altair_chart(chart, use_container_width=True)
      
    # Define the second element in the second row   
    with col5:
        # Display message
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none; font-weight: bold;text-align: left;'> Steady-State Loop [B-H]</span>""", unsafe_allow_html=True)

        # Plot setting  
        chart2 = draw_line(B, H)
        st.altair_chart(chart2, use_container_width=True)
  
    # Define the third element in the second row   
    with col6:
        # Display message
        st.write("""<span style='font-size: calc(0.6vw + 0.6vh + 10px); text-decoration: none;font-weight: bold;text-align: left;'> Volumetric Loss [Pv]</span>""", unsafe_allow_html=True)

        # Customize a textbox 
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
        
        # Display customize metric container
        if sum(B) == 0:
            st.markdown(f'<div class="metric-container"><h1>Unknown</h1><p>kW/m³</p></div>', unsafe_allow_html=True)   
            
            # Add blank space  
            st.markdown("<div style='height:2vh;'></div>", unsafe_allow_html=True)
            
            # Add left margin to the download button
            _, col6_1 = st.columns([1.4, 1])
            with col6_1:
                # Disabled download button
                text_contents = '''Error occurs during downloading'''
                st.download_button("Download\n\n 📂", text_contents, disabled=True)
        else: 
            # Display message
            st.markdown(f'<div class="metric-container"><h1>{round(P/1000, 2)}</h1><p>kW/m³</p></div>', unsafe_allow_html=True)
            
            # Add blank space 
            st.markdown("<div style='height:2vh;'></div>", unsafe_allow_html=True)
            
            # Add left margin to the download button
            _, col6_1 = st.columns([1.4, 1])
            
            # Create the csv file for the predicted results             
            with col6_1:
                df = DataFrame(columns=['B [mT]','H [A/m]','Pv [W/m3]'])
                df['B [mT]'] = B
                df['H [A/m]'] = H
                df['Pv [W/m3]'] = [P] + [None] * (len(B) - 1)
                csv = df.to_csv()
                
                # Display the download button
                st.download_button(
                    label="Download 📂",
                    help="Download B-H-Pv in " + str(resolution_params[model]) + " step as CSV",
                    data=csv.encode('utf-8'),
                    file_name='magnet-engine_prediction.csv',
                    use_container_width = True,
                    mime='text/csv',
                )

# Main program
if __name__ == "__main__":
    main()
    footer()

