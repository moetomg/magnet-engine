"""
File contains grab-bag of utility functions and objects.

Source: https://github.com/moetomg/magnet-engine
"""
import altair as alt 
import magnethub as mh

from pandas import DataFrame

def load_model(model, material):
    """
    Load the core loss model from magnet-hub.
    
    Args:
        model (torch.nn): The trained core loss model. 
        material (string): The name of the material.
    """    
    mdl = mh.loss.LossModel(material, model)
    return mdl

def draw_donut(input_response, input_text, input_color, range=[50,450]):
    """
    Draw a donut plot to visualize data.
    
    Args:
        input_response (float): The input data. 
        input_text (string): The name of the input variable.
        input_color (string): The color style.
        range (list): The value range of the variable.
    """ 
    # Select the color style including the foreground color and background color
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
    
    # Define the input ratio
    ratio = round((input_response-range[0])/(range[1]-range[0])*100)

    # Put the input and the input ratio into the data frames
    source = DataFrame({
        "Topic": ['', input_text],
        "% value": [100-ratio, ratio]
    })
    source_bg = DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })
   
    # Plot the donut foreground     
    plot = alt.Chart(source).mark_arc(innerRadius=40, cornerRadius=22).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),
                        legend=None),
    ).properties(width=128, height=128)

    # Display the input value           
    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=30, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response}'))
    
    # Plot the donut background  
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=40, cornerRadius=22).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=128, height=128)
    return plot_bg + plot + text

def draw_line(flux, field, time=None):
    """
    Draw a line plot to visualize B-H curves.
    
    Args:
        flux (np.array): The magnetic flux density (B).
        field (np.array): The magnetic field strength (H).
        time (np.array): The time sequence (t).
    """ 
    # Define the dataframe 
    df = DataFrame(columns=['t', 'B', 'H'])
    df['t'] = time
    df['B'] = flux
    df['H'] = field

    # Plot discrete sequences for B and H
    if time is not None:
        base = alt.Chart(df.reset_index()).encode(x=alt.X('t', title='Fraction of a Cycle', axis=alt.Axis(titlePadding=14, titleFontWeight='bold')))
        chart = alt.layer(
            base.mark_line(strokeWidth=5, stroke='#8E2DE2').encode(y=alt.X('B', title='B [mT]', axis=alt.Axis(titlePadding=0, titleFontWeight='bold', grid=True, titleColor='#8E2DE2'))),
            base.mark_line(strokeWidth=5, stroke='#E74C3C').encode(y=alt.X('H', title='H [A/m]', axis=alt.Axis(titlePadding=10, titleFontWeight='bold', grid=True, gridDash=[3, 3], titleColor='#E74C3C')))
        ).resolve_scale(y='independent').properties(height=330)
    # Plot the predicted B-H curve
    else: 
        chart = alt.Chart(df[['B', 'H']]).mark_line(strokeWidth=5, stroke='#29b5e8').encode(
            x = alt.X('H', title='H [A/m]', axis=alt.Axis(titlePadding=5, titleFontWeight='bold', grid=True), sort=None, \
                scale=alt.Scale(domain=(round(min(field) - 0.05 * (max(field) - min(field))), round(max(field) + 0.05 * (max(field) - min(field)))))),
            y = alt.Y('B', title='B [mT]', axis=alt.Axis(titlePadding=0, titleFontWeight='bold', grid=True)), 
        ).properties(height=330)
        
    # Show the grid  
    chart = chart.configure_axis(grid=True)
    return chart 

def generateTriSequence(time, amplitude, phase, duty):
    """
    Generate a triangular excitation waveform.
    
    Args:
        time (np.array): The time discrete sequence. 
        amplitude (float): The amplitude of the input excitation.
        phase (float): The inital phase angle of the input excitation.
        duty (float): The duty cycle of the rising curve.
    """ 
    # Allocate cache for the output data
    yData = []
    
    # Correct the initial phase angle 
    phase = (-phase - duty * 180) % 360

    # Generate input discrete sequence
    for i in range(len(time)): 
        if (duty + phase / 360) <= 1:
            if time[i] <= phase / 360:
                yData.append(-amplitude + (phase / 360 - time[i]) * (2 * amplitude) / (1 - duty))
            elif time[i] <= phase / 360 + duty:
                yData.append(-amplitude + (time[i] - phase / 360) * (2 * amplitude) / duty)
            else:
                yData.append(amplitude - (time[i] - phase / 360 - duty) * (2 * amplitude) / (1 - duty))      
        else:
            if (time[i] <= phase / 360 - (1 - duty)):
                yData.append(amplitude - (phase / 360 - (1 - duty) - time[i]) * (2 * amplitude) / duty)
            elif(time[i] <= phase / 360):
                yData.append(amplitude - (time[i] - (phase / 360 - (1 - duty))) * (2 * amplitude) / (1 - duty))
            else:
                yData.append(-amplitude + (time[i] - phase / 360) * (2 * amplitude) / duty)
    return yData

def generateTrapSequence(time, amplitude, phase, duty1, duty2):
    """
    Generate a trapzoidal excitation waveform.
    
    Args:
        time (np.array): The time discrete sequence. 
        amplitude (float): The amplitude of the input excitation.
        phase (float): The inital phase angle of the input excitation.
        duty1 (float): The duty cycle of the rising curve.
        duty2 (float): The duty cycle of the floating curve.
    """ 
    # Allocate cache for the output data
    yData = []
    
    # Correct the initial phase angle 
    phase = (-phase - duty1 * 180) % 360
    
    # Generate input discrete sequence
    for i in range(len(time)):
        if (phase / 360) <= (1 - duty1 - duty2) / 2:
            if time[i] <= phase / 360:
                yData.append(-amplitude)
            elif time[i] <= phase / 360 + duty1:
                yData.append(-amplitude + (time[i] - phase / 360) * (2 * amplitude) / duty1)
            elif time[i] <= phase / 360 + duty1 + (1 - duty1 - duty2) / 2:
                yData.append(amplitude)
            elif time[i] <= phase / 360 + duty1 + (1 - duty1 - duty2) / 2 + duty2:
                yData.append(amplitude - (time[i] - (phase / 360 + duty1 + (1 - duty1 - duty2) / 2)) * (2 * amplitude) / duty2) 
            else:
                yData.append(-amplitude)
             
        elif(phase / 360) <= (1 - duty1 - duty2) / 2 + duty2:
            if (time[i] <= phase / 360 - ((1 - duty1 - duty2) / 2)): 
                yData.append(-amplitude + ((phase / 360 - (1 - duty1 - duty2) / 2) - time[i]) * (2 * amplitude) / duty2) 
            elif (time[i] <= phase / 360):
                yData.append(-amplitude) 
            elif (time[i] <= phase / 360 + duty1):
                yData.append(-amplitude + (time[i] - phase / 360) * (2 * amplitude) / duty1) 
            elif (time[i] <= phase / 360 + duty1 + (1 - duty1 - duty2) / 2):
                yData.append(amplitude) 
            else:
                yData.append(amplitude - (time[i] - (phase / 360 + duty1 + (1 - duty1 - duty2) / 2)) * (2 * amplitude) / duty2)
            
        elif (phase / 360) <= (1 - duty1 - duty2) + duty2:
            if (time[i] <= phase / 360 - (1 - duty1 - duty2) / 2 - duty2):
                yData.append(amplitude)
            elif (time[i] <= phase / 360 - (1 - duty1 - duty2) / 2):
                yData.append(amplitude - (time[i] - (phase / 360 - (1 - duty1 - duty2) / 2 - duty2)) * (2 * amplitude) / duty2)
            elif (time[i] <= phase / 360):
                yData.append(-amplitude)
            elif (time[i] <= phase / 360 + duty1):
                yData.append(-amplitude + (time[i] - phase / 360) * (2 * amplitude) / duty1)
            else:
                yData.append(amplitude)
            
        else:
            if (time[i] <= phase / 360 - (1 - duty1 - duty2) - duty2):
                yData.append(amplitude - ((phase / 360 - (1 - duty1 - duty2) - duty2) - time[i]) * (2 * amplitude) / duty1)
            elif (time[i] <= phase / 360 - (1 - duty1 - duty2) / 2 - duty2):
                yData.append(amplitude)
            elif (time[i] <= phase / 360 - (1 - duty1 - duty2) / 2):
                yData.append(amplitude - (time[i] - (phase / 360 - (1 - duty1 - duty2) / 2 - duty2)) * (2 * amplitude) / duty2)
            elif (time[i] <= phase / 360):
                yData.append(-amplitude)
            else:
                yData.append(-amplitude + (time[i] - phase / 360) * (2 * amplitude) / duty1)
    return yData      