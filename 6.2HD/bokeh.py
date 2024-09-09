from bokeh.io import output_file, show, output_notebook, curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, DatetimeTickFormatter, TextInput, Button, DataTable, TableColumn, HoverTool,Div
from bokeh.plotting import figure 
from bokeh.models import CustomJS, RangeSlider, Range1d
from bokeh.io import push_notebook
import numpy as np
import pandas as pd
from datetime import datetime
import os

df = pd.read_csv('data_file.csv') #Read the csv file
df.drop(columns = {'id'}, inplace = True) #Drop irrelevant column
df.timestamp = pd.to_datetime(df.timestamp) #Convert timestamp to datetime


curdoc().theme = 'caliber'

# =========================== Create a plot and declare plot =====================
plot = figure(
    title="Simple Plot",
    x_axis_type='datetime',
    x_axis_label='Timestamp',
    y_axis_label='y',
    width=620,
    height=500,
)
line_renderer = plot.line(df.timestamp, df.x,line_width=2, color='blue')
scatter_renderer = plot.scatter(df['x'], df['y'], size=10, color="navy", alpha=0.5, legend_label="Scatter", visible=False)
bar_renderer = plot.vbar(x=df.timestamp, top=df.x, width=0.9, color="skyblue")
area_renderer = plot.varea(x=df['timestamp'][0:10], 
                                       y1=[0]*10, 
                                       y2=df['x'][0:10], fill_color="skyblue")

#Visible the linew plot
for i in range(2):
    plot.renderers[i+1].visible = False

header = Div(text="<h1 style=' color: darkblue; text-align: center;'>Plotting using Bokeh</h1>", width=400, height=50)
description = Div(text="<p>This is the simple plot using Bokeh, in this web you can select the type of different graph and select the first variable for Line, Area, Bar and choose 2 variable for Scatter Plot. The Previous and Next buttons is used to go through the x-axis and the Reset button will use to reset back to 10 samples. After  a certain seconds the samples will be saved to CSV file. Moreover, these is a summary table for statistical measures for each numbers of samples<p>", width=620, height=90)
#============================== Widget declaration==============================
#Add the graph selection
select_graph = Select(title="<h3>Select Plot Type</h3>", value="Line graph", options=["Line graph", "Area plot", "Bar plot", "Scatter Plot"], width=620)
#Add the variable selection
select_var = Select(title="Select variable for y-axis/variable 1", value="X", options=["X", "Y", "Z", "All"], width=305)
#Add the variable selection
select_var_2 = Select(title="Select variable 2", value="Y", options=["X", "Y", "Z"], width=305)
# Text input for the number of samples
sample_input = TextInput(value="10", title="Number of samples:", width=620)
# Buttons for navigtion
prev_button = Button(label="Previous", button_type="success", width=200)
next_button = Button(label="Next", button_type="success", width=200)
reset_button = Button(label="Reset", button_type="danger", width=200)
status = Div(text="No new data yet")
countdown_div = Div(text="Time until next update: 10 seconds", width=600, height=30)
timer_input = TextInput(value="10", title="Time for countdown:", width=620)
#============================== Data Table ======================================
stats = df.describe().reset_index()
stats_source = ColumnDataSource(stats)
# Create DataTable for data summary
columns = [
    TableColumn(field="index", title="Statistical Measure"),
    TableColumn(field="timestamp", title="Timestamp"),
    TableColumn(field="x", title="x"),
    TableColumn(field="y", title="y"),
    TableColumn(field="z", title="z")
]
data_table = DataTable(source=stats_source, columns=columns, width=600, height=280)

#===================== Select graphs function callback ========================
# Initialize the global start index
current_ren = "Line graph"
current_var = "x"
current_var_2 = "y"
start_index = 0
countdown_timer = int(timer_input.value) # Countdown timer for updating data

def update_plot():
    global start_index
    global df_subset
    num_samples = int(sample_input.value)

    # Ensure start_index is within bounds
    start_index = max(0, min(start_index, len(df) - num_samples))
    
    # Get the end index
    end_index = start_index + num_samples
    
    df_subset = df.iloc[start_index:end_index]
    plot.renderers = []
    for var, color in zip(current_var, ['steelblue', 'olivedrab', 'mediumaquamarine']):
        if (current_ren == "Line graph"):
            line_renderer = plot.line(df_subset.timestamp, df_subset[var],line_width=2, color=color, legend_label=var)
        elif (current_ren == "Area plot"):
            area_renderer = plot.varea(x=df['timestamp'][start_index:end_index], 
                                       y1=[0]*(end_index-start_index), 
                                       y2=df['x'][start_index:end_index], fill_color="skyblue")
        elif (current_ren == "Bar plot"):
            bar_renderer = plot.vbar(x=df_subset['timestamp'], top= df_subset[var], width=5, color=color, legend_label=var)
        elif (current_ren == "Scatter Plot"):
            scatter_renderer = plot.scatter(df_subset[var], df_subset[current_var_2.lower()], size=10, color="navy", alpha=0.5, legend_label="Scatter", visible=True)
    # Update the data source
    stats_source.data = df_subset.describe().reset_index()  
    

# =========================== Add Hover Tool ============================
    tooltips = [("Timestamp", "@x{%H:%M:%S}"), ("Value", "@y")]
    hover = HoverTool(tooltips = tooltips, mode='vline', formatters = {'@x': 'datetime'})
    plot.add_tools(hover)

#===================== Button function callback ========================
def prev_samples():
    global start_index
    num_samples = int(sample_input.value)
    start_index = max(0, start_index - num_samples)
    update_plot()

def next_samples():
    global start_index
    num_samples = int(sample_input.value)
    start_index = min(len(df) - num_samples, start_index + num_samples)
    update_plot()

def reset_samples():
    global start_index
    start_index = 0
    sample_input.value = "10";
    update_plot()

#===================== Select graph function callback ========================
def update_renderer(attr, old, new):
    global current_ren 
    current_ren = select_graph.value
    update_plot()
#===================== Select variable function callback ========================
def update_variable(attr, old, new):
    global current_var
    global current_var_2
    current_var = select_var.value
    current_var_2 = select_var_2.value
    if (select_var.value == "X"):
        current_var = "x"
    elif (select_var.value == "Y"):
        current_var = "y"
    elif (select_var.value == "Z"):
        current_var = "z"
    elif (select_var.value == "All"):
        current_var = ["x", "y", "z"]  
    update_plot()

# Function to update data
def update_data():
    global df_subset
    df_subset.to_csv("bokeh.csv", index=False, header=True)
    if os.path.exists("bokeh.csv"):
        df_subset = pd.read_csv("bokeh.csv")
        status.text = "New data loaded!"

# Function to update the countdown timer
def update_countdown():
    global countdown_timer
    if countdown_timer > 0:
        countdown_timer -= 1
    else:
        update_data()
        countdown_timer = int(timer_input.value)
    countdown_div.text = f"Time until next update: {countdown_timer} seconds"

# Attach the update function to the text input and buttons
sample_input.on_change('value', lambda attr, old, new: update_plot())
timer_input.on_change('value', lambda attr, old, new: update_countdown())
prev_button.on_click(prev_samples)
next_button.on_click(next_samples)    
reset_button.on_click(reset_samples)
# Initialize variables
select_var.on_change('value', update_variable)
select_var_2.on_change('value', update_variable)
select_graph.on_change('value', update_renderer)
update_plot()

# Create a layout and show it in the notebook
curdoc().add_periodic_callback(update_countdown, countdown_timer*100)
layout = column(header,
                description,
                select_graph, 
                row(select_var, select_var_2),
                sample_input, 
                row(prev_button, next_button, reset_button),
                timer_input,
                status,
                countdown_div, 
                plot, data_table)
curdoc().add_root(layout)