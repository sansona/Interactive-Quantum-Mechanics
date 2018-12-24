#!/usr/bin/python3
import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider, BoxAnnotation
from bokeh.plotting import figure, output_file, show, ColumnDataSource


# -----------------------------------------------------------------------------


def generate_wavedata(L=1):
    '''
    generates dictionaries for energy level, wavefunction, and probability
    densities for  all [0, L]

    Data feeds into generate_n_callback
    '''
    x = np.linspace(0, L, 1000)
    # initialize E to small initial energy to show n**2 behavior. Following
    # correspond to energy levels for n=2 & n=3
    E = np.ones(1000)*0.3
    E2 = E*4
    E3 = E*9

    phi = np.sqrt(2/L)*np.sin((np.pi*x)/L)
    prob_density = phi**2

    E_source = ColumnDataSource(data=dict(x=x, y=E))
    E2_source = ColumnDataSource(data=dict(x=x, y=E2))
    E3_source = ColumnDataSource(data=dict(x=x, y=E3))

    E_list = [E_source, E2_source, E3_source]

    phi_source = ColumnDataSource(data=dict(x=x, y=phi))
    prob_source = ColumnDataSource(data=dict(x=x, y=prob_density))

    return E_list, phi_source, prob_source


# -----------------------------------------------------------------------------


def generate_n_plot(E_col, phi_col, prob_col, y_range=(-3, 3), size=750):
    '''
    generates initial plot with starting values of E, phi, & probability density. generate_callbacks updates this plot 
    '''
    plot = figure(y_range=y_range, plot_width=size, plot_height=size,
                  title='Wavefunction, Probability Density, and Energy')
    plot.yaxis.visible = False
    plot.xaxis.axis_label = 'x'
    plot.xaxis.axis_label_text_font_size = '24pt'
    plot.line('x', 'y', source=E_col, line_width=6,
              color='olive', line_alpha=0.6, legend='E(n=1)')
    plot.line('x', 'y', source=phi_col, line_width=6,
              line_alpha=0.6, legend='Phi')
    plot.line('x', 'y', source=prob_col,
              color='red', line_width=6, line_alpha=0.6,
              legend='Probability density')
    left_quad = BoxAnnotation(left=0, right=0.25,
                              fill_color='blue', fill_alpha=0.1)

    right_quad = BoxAnnotation(left=0.5, right=0.75,
                               fill_color='blue', fill_alpha=0.1)

    plot.add_layout(left_quad)
    plot.add_layout(right_quad)

    plot.legend.location = 'top_left'
    plot.legend.click_policy = 'hide'

    return plot

# -----------------------------------------------------------------------------


def generate_L_plot(E_col_list, y_range=(-1, 15), size=750):
    '''
    generates initial plot with starting values of E corresponding to n=1,2,3. 
    Shows increasting energy gaps as n decreases
    '''
    plot = figure(y_range=y_range, plot_width=size,
                  plot_height=size, title='Energy levels n=1,2,3')
    plot.xaxis.axis_label = 'x'
    plot.xaxis.axis_label_text_font_size = '24pt'
    plot.yaxis.axis_label = 'E'
    plot.yaxis.axis_label_text_font_size = '24pt'
    plot.line([0, 1], [0, 0], color='black', line_width=3, legend='E=0')
    plot.line('x', 'y', source=E_col_list[0], line_width=6,
              color='olive', line_alpha=0.6, legend='E(n=1)')
    plot.line('x', 'y', source=E_col_list[1], line_width=6,
              line_alpha=0.6, legend='E(n=2)')
    plot.line('x', 'y', source=E_col_list[2],
              color='red', line_width=6, line_alpha=0.6,
              legend='E(n=3)')
    plot.legend.location = 'top_left'
    plot.legend.click_policy = 'hide'

    return plot
# -----------------------------------------------------------------------------


def generate_callbacks(phi_col, prob_col, E_col_list):
    '''
    establish formulas for updating plots. Generates sliders corresponding to
    n & l. Browser executables written in JavaScript

    type(*_col) == dict
    '''
    n_callback = CustomJS(args=dict(
        source=phi_col, source2=prob_col, source3=E_col_list[0]),
        code="""
        var data = source.data;
        var n = cb_obj.value
        var L = 1
        var x = data['x']
        var phi = data['y']
        for (var i = 0; i < x.length; i++) {
            phi[i] = Math.sqrt(2/L)*Math.sin((n*Math.PI*x[i])/L);
        }
        var data2 = source2.data
        var prob = data2['y']
        for (var i = 0; i < x.length; i++) {
            prob[i] = Math.pow(Math.sqrt(2/L)*Math.sin((n*Math.PI*x[i])/L), 2);
        }
        var data3 = source3.data
        var E = data3['y']
        for (var i = 0; i < x.length; i++) {
            E[i] = 0.1*Math.pow(n, 2);    
        }
        source.change.emit();
    """)

    L_callback = CustomJS(args=dict(
        source=E_col_list[0], source2=E_col_list[1], source3=E_col_list[2]),
        code="""
        var data = source.data;
        var L = cb_obj.value
        var x = data['x']
        var E1 = data['y']
        for (var i = 0; i < x.length; i++) {
            E1[i] = 0.3/Math.pow(L, 2);  
        }
        var data2 = source2.data
        var E2 = data2['y']
        for (var i = 0; i < x.length; i++) {
            E2[i] = 1.2/Math.pow(L, 2);  
        }
        var data3 = source3.data
        var E3 = data3['y']
        for (var i = 0; i < x.length; i++) {
            E3[i] = 2.7/Math.pow(L, 2);    
        }
        source.change.emit();
    """)

    n_slider = Slider(start=1, end=100, value=1, step=1,
                      title='n', callback=n_callback)
    L_slider = Slider(start=0.1, end=10, value=1, step=0.1,
                      title='L', callback=L_callback)

    return n_slider, L_slider

# -----------------------------------------------------------------------------


def return_graphics():
    E_list, phi_wave, prob_wave = generate_wavedata()
    n_plot = generate_n_plot(E_list[0], phi_wave, prob_wave)
    L_plot = generate_L_plot(E_list)
    n_slider, L_slider = generate_callbacks(phi_wave, prob_wave, E_list)
    layout = row(n_plot, L_plot, widgetbox(n_slider, L_slider))

    show(layout)


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    return_graphics()
