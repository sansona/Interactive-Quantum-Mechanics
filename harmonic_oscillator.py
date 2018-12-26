#!/usr/bin/python3
import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider, BoxAnnotation
from bokeh.plotting import figure, output_file, show, ColumnDataSource

# -----------------------------------------------------------------------------


def generate_oscillator_data(L=5):

    x = np.linspace(-L, L, 1000)
    y = x**2
    E = 2

    harmonic_source = ColumnDataSource(data=dict(x=x, y=y))

    return harmonic_source


# -----------------------------------------------------------------------------
def generate_energy_levels(delta=2):
    x_coords = []
    E_levels = []
    energy_source_list = []

    for i in range(24):
        x_coords.append(np.linspace(-np.sqrt(i+delta), np.sqrt(i+delta), 1000))
        E_levels.append(np.ones(1000)*(i+delta))

    for i in range(len(x_coords)):
        energy_source_list.append(ColumnDataSource(data=dict(x=x_coords[i],
                                                             y=E_levels[i])))

    return energy_source_list

# -----------------------------------------------------------------------------


def generate_harmonic_plot(harmonic_col, energy_source_list, y_range=(0, 25),
                           L=5, size=750):

    plot = figure(y_range=y_range, plot_width=size, plot_height=size,
                  title='Energy levels of harmonic oscillator')
    plot.yaxis.visible = False
    plot.xaxis.axis_label = 'x'
    plot.xaxis.axis_label_text_font_size = '24pt'

    plot.line('x', 'y', source=harmonic_col, line_width=6,
              color='blue', line_alpha=0.6,
              legend='Harmonic oscillator potential')

    for i in range(len(energy_source_list)):
        plot.line('x', 'y', source=energy_source_list[i], line_width=3,
                  line_alpha=0.6, legend='n=%s' % (i+1))

    plot.legend.location = 'top_left'
    plot.legend.click_policy = 'hide'

    return plot
# -----------------------------------------------------------------------------


def generate_callbacks(harmonic_col):

    n_callback = CustomJS(args=dict(
            source=harmonic_col),
            code="""
		var data = source.data;
		var n = cb_obj.value
		var x = data['x']
		var E = data['y']
		for (var i = 0; i < x.length; i++) {
			E[i] = 2*n
		}

		source.change.emit();
	""")

    n_slider = Slider(start=1, end=10, value=1, step=1,
                      title='n', callback=n_callback)

    return n_slider
# -----------------------------------------------------------------------------


def return_graphics():
    harmonic_wave = generate_oscillator_data()
    energy_list = generate_energy_levels()
    n_plot = generate_harmonic_plot(harmonic_wave, energy_list)
    n_slider = generate_callbacks(harmonic_wave)
    layout = row(n_plot, widgetbox(n_slider))

    show(layout)

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    return_graphics()
