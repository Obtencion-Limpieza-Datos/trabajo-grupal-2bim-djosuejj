''' Present an interactive function explorer with slider widgets.

Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.

Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve sliders.py

at your command prompt. Then navigate to the URL

    http://localhost:5006/sliders

in your browser.

'''
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
import pandas as pd

# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))


### Leer CSV
mi_df = pd.read_csv('info.csv',encoding="latin-1",sep=";")
counts = [10, 12, 4, 22]

source = ColumnDataSource(data=dict(fruits=mi_df.Ciudad, counts=mi_df.Poblacion))


plot = figure(x_range=mi_df.Ciudad, plot_height=350, toolbar_location=None, 
        tools="crosshair,pan,reset,save,wheel_zoom",
        title="Ciuades")
plot.vbar(x='fruits', top='counts', width=0.9, source=source, legend="fruits",
       line_color='white', fill_color=factor_cmap('fruits', palette=Spectral6, factors=mi_df.Ciudad))


plot.xgrid.grid_line_color = None
plot.y_range.start = 0
plot.y_range.end = 450000
plot.legend.orientation = "horizontal"
plot.legend.location = "top_center"



# Set up widgets
text = TextInput(title="title", value=u'mi gráfica')
v1 = Slider(title="Loja", value=0.0, start=1000.0, end=200000, step=5000.0)
v2 = Slider(title="Quito", value=0.0, start= 10000.0, end=300000, step=5000.0)
v3 = Slider(title="Guayaquil", value=0.0, start=1000.0, end=30000, step=5000.0)
v4 = Slider(title="Cuenca", value=0.0, start=1000.0, end=20000, step=5000.0)



# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    a = v1.value
    b = v2.value
    w = v3.value
    k = v4.value


    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)
    y = a*np.sin(k*x + w) + b
    
    fruits = ['Loja', 'Quito', 'Guayaquil', 'Cuenca']
    counts = [a, b, w, k]
    source.data = dict(fruits=mi_df.Ciudad, counts=mi_df.Poblacion)

for w in [v1, v2, v3, v4]:
    w.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(text, v1, v2, v3, v4)

curdoc().add_root(row(inputs, plot, width=100000))
curdoc().title = "Sliders"
