#!/usr/bin/python3
import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider, BoxAnnotation
from bokeh.plotting import figure, output_file, show, ColumnDataSource

# -----------------------------------------------------------------------------


def generate_oscillator_data(L=5):
    '''
    generates dict of data for harmonic oscillator potential

    Feeds into generate_harmonic_plot
    '''

    x = np.linspace(-L, L, 1000)
    y = x**2
    x2 = np.linspace(-1, 10, 1000)
    y2 = np.ones(1000)*(1-np.exp(-x2))**2
    E = 2

    harmonic_source = ColumnDataSource(data=dict(x=x, y=y))
    anharmonic_source = ColumnDataSource(data=dict(x=x2, y=y2))

    return harmonic_source, anharmonic_source


# -----------------------------------------------------------------------------

def generate_energy_levels(delta=2):
    '''
    generates dicts for energy levels of delta n 
    '''
    x_coords = []
    E_levels = []
    energy_source_list = []

    for i in range(0, 13):
        x_coords.append(np.linspace(-np.sqrt(i*delta), np.sqrt(i*delta), 1000))
        E_levels.append(np.ones(1000)*(i*delta))

    for i in range(len(x_coords)):
        energy_source_list.append(ColumnDataSource(data=dict(x=x_coords[i],
                                                             y=E_levels[i])))

    return energy_source_list

# -----------------------------------------------------------------------------


def generate_harmonic_plot(harmonic_col, energy_source_list, y_range=(0, 25),
                           L=5, size=750):

    plot = figure(y_range=y_range, plot_width=size, plot_height=size,
                  title='Energy levels of harmonic oscillator')
    plot.yaxis.axis_label = 'E'
    plot.yaxis.axis_label_text_font_size = '24pt'
    plot.xaxis.axis_label = 'r - r0'
    plot.xaxis.axis_label_text_font_size = '24pt'

    plot.line('x', 'y', source=harmonic_col, line_width=6,
              color='blue', line_alpha=1,
              legend='Harmonic oscillator potential')

    for i in range(1, len(energy_source_list)):
        if i == 1:
            plot.line('x', 'y', source=energy_source_list[i],
                      line_width=3, line_alpha=0.8, color='red',
                      legend='Zero point energy (E(n=1))')
        if i in range(2, 5):
            plot.line('x', 'y', source=energy_source_list[i],
                      line_width=3, line_alpha=0.8, color='red',
                      legend='E(n=%s)' % i)
        else:
            plot.line('x', 'y', source=energy_source_list[i], line_width=3,
                      line_alpha=0.8, color='red')

    positive_marker = BoxAnnotation(bottom=0, top=100,
                                    fill_color='blue', fill_alpha=0.05)
    plot.add_layout(positive_marker)

    plot.legend.location = 'top_left'
    plot.legend.click_policy = 'hide'

    return plot
# -----------------------------------------------------------------------------


def generate_anharmonic_plot(anharmonic_col, y_range=(0, 2), L=5, size=750):
    plot = figure(y_range=y_range, plot_width=size, plot_height=size,
                  title='Energy levels of anharmonic oscillator')
    plot.yaxis.axis_label = 'E'
    plot.yaxis.axis_label_text_font_size = '24pt'
    plot.xaxis.axis_label = 'r - r0'
    plot.xaxis.axis_label_text_font_size = '24pt'
    plot.line('x', 'y', source=anharmonic_col, line_width=6,
              color='blue', line_alpha=1,
              legend='Anharmonic oscillator potential')
    positive_marker = BoxAnnotation(bottom=0, top=100,
                                    fill_color='blue', fill_alpha=0.05)
    plot.add_layout(positive_marker)

    return plot

# -----------------------------------------------------------------------------


def return_graphics():
    harmonic_wave, anharmonic_wave = generate_oscillator_data()
    energy_list = generate_energy_levels()
    n_plot = generate_harmonic_plot(harmonic_wave, energy_list)
    an_plot = generate_anharmonic_plot(anharmonic_wave)

    layout = row(n_plot, an_plot)
    show(layout)

# -----------------------------------------------------------------------------


if __name__ == '__main__':
    return_graphics()
