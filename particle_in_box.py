import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider
from bokeh.plotting import figure, output_file, show, ColumnDataSource

L = 1  # if change this, need to reflect in JS code to reflct. See line 20
x = np.linspace(0, L, 100)
y = np.sqrt(2/L)*np.sin((3*3.14*x)/L)

source = ColumnDataSource(data=dict(x=x, y=y))

plot = figure(y_range=(-10, 10), plot_width=750, plot_height=750)

plot.line('x', 'y', source=source, line_width=6, line_alpha=0.6)

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var n = cb_obj.value
    var L = 1
    var x = data['x']
    var y = data['y']
    for (var i = 0; i < x.length; i++) {
        y[i] = Math.sqrt(2/L)*Math.sin((n*3.14*x[i])/L);
    }
    source.change.emit();
""")

slider = Slider(start=1, end=100, value=1, step=1, title='n')
slider.js_on_change('value', callback)


layout = row(plot, widgetbox(slider))

output_file("particle_in_box.html", title="particle_in_box.py plot")

show(layout)
