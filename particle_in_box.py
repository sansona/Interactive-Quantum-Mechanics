#!/usr/bin/python3
import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider, BoxAnnotation
from bokeh.plotting import figure, output_file, show, ColumnDataSource


# -----------------------------------------------------------------------------
# Generates interactive graphic for 1D particle in box. Graphics allow user
# to visualize the relationship between the wavefunction, the probability
# density, length of box, energy levels, and average positions.
#
# Code is admittedly very spaghetti. Bokeh makes writing multiple interactive
# sliders somewhat complicated and messy, but hey, it works!
# -----------------------------------------------------------------------------

def generate_wavedata(L=1):
    '''
    generates dictionaries for energy level, wavefunction, and probability
    densities for  all [0, L]

    If change L, need to reflect changes in JS code in generate_callback

    Data feeds into generate_callback
    '''
    x = np.linspace(0, L, 1000)
    # calculating variance in position
    x_av = np.ones(1000)*L/2
    a_av = np.ones(1000)*L*np.sqrt(1/12 - 1/(2*(np.pi)**2))

    y_av = np.linspace(0, L, 1000)
    # initialize E to small initial energy to show n**2 behavior. Following
    # correspond to energy levels for n=2 & n=3
    E = np.ones(1000)*0.3
    E2 = E*4
    E3 = E*9

    phi = np.sqrt(2/L)*np.sin((np.pi*x)/L)
    prob_density = phi**2

    # *_source correspond to dicts of x & y that are fed into the plots
    x_av_source = ColumnDataSource(data=dict(x=x_av, y=y_av))
    av_source = ColumnDataSource(data=dict(x=a_av, y=y_av))
    E_source = ColumnDataSource(data=dict(x=x, y=E))
    E2_source = ColumnDataSource(data=dict(x=x, y=E2))
    E3_source = ColumnDataSource(data=dict(x=x, y=E3))
    E_list = [E_source, E2_source, E3_source]

    phi_source = ColumnDataSource(data=dict(x=x, y=phi))
    prob_source = ColumnDataSource(data=dict(x=x, y=prob_density))

    return x_av_source, av_source, E_list, phi_source, prob_source


# -----------------------------------------------------------------------------


def generate_n_plot(x_col, av_col, E_col, phi_col, prob_col,
                    y_range=(-5, 5), L=1, size=750):
    '''
    generates initial plot with starting values of E, phi, & probability density. generate_callbacks updates this plot 
    '''
    plot = figure(y_range=y_range, plot_width=size, plot_height=size,
                  title='Wavefunction, Probability Density, and Energy.')
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
    plot.line('x', 'y', source=x_col, line_width=3,
              color='purple', line_alpha=0.6, legend='Average position (L/2')
    plot.line('x', 'y', source=av_col, line_width=3,
              color='black', line_alpha=0.6, legend='Variance from L/2')
    left_marker = BoxAnnotation(left=L/4-0.005, right=L/4,
                                fill_color='gray', fill_alpha=0.3)
    center_marker = BoxAnnotation(left=L/2-0.005, right=L/2,
                                  fill_color='gray', fill_alpha=0.3)
    right_marker = BoxAnnotation(left=L*(3/4)-0.005, right=L*(3/4),
                                 fill_color='gray', fill_alpha=0.3)
    positive_marker = BoxAnnotation(bottom=0, top=100,
                                    fill_color='blue', fill_alpha=0.05)
    negative_marker = BoxAnnotation(bottom=-100, top=0,
                                    fill_color='red', fill_alpha=0.01)

    plot.add_layout(left_marker)
    plot.add_layout(center_marker)
    plot.add_layout(right_marker)
    plot.add_layout(positive_marker)
    plot.add_layout(negative_marker)

    plot.legend.location = 'top_left'
    plot.legend.click_policy = 'hide'

    return plot

# -----------------------------------------------------------------------------


def generate_L_plot(E_col_list, size=750, L=1):
    '''
    generates initial plot with starting values of E corresponding to n=1,2,3. 
    Shows increasting energy gaps as n decreases

    '''
    plot = figure(y_range=(-1, L+20), plot_width=size,
                  plot_height=size, title='Energy levels n=1,2,3')
    plot.xaxis.axis_label = 'x'
    plot.xaxis.axis_label_text_font_size = '24pt'
    plot.yaxis.axis_label = 'E'
    plot.yaxis.axis_label_text_font_size = '24pt'
    plot.line([0, L], [0, 0], color='black', line_width=3, legend='E=0')
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


def generate_callbacks(x_col, av_col, phi_col, prob_col, E_col_list):
    '''
    establish formulas for updating plots. Generates sliders corresponding to
    n & L. Browser executables written in JavaScript

    If change L, need to reflect changes in line 128

    type(*_col) == dict
    '''
    n_callback = CustomJS(args=dict(
        source=phi_col, source2=prob_col,
        source3=E_col_list[0], source4=av_col),
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
        var data4 = source4.data
        var av = data4['x']
        for (var i = 0; i < av.length; i++) {
            av[i] = L*Math.sqrt(1/12 - 1/(2*Math.pow(Math.PI, 2)*Math.pow(n, 2)))
        }

        source.change.emit();
    """)

    L_callback = CustomJS(args=dict(
        source=E_col_list[0], source2=E_col_list[1],
        source3=E_col_list[2], source4=phi_col,
        source5=prob_col, source6=av_col, source7=x_col),
        code="""
        var data = source.data
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
        var data4 = source4.data
        var x4 = data4['x']
        var phi = data4['y']
        for (var i = 0; i < x4.length; i++) {
            phi[i] = Math.sqrt(2/L)*Math.sin((Math.PI*x4[i])/L);
        }
        var data5 = source5.data
        var x5 = data5['x']
        var prob = data5['y']
        for (var i = 0; i < x5.length; i++) {
            prob[i] = Math.pow(Math.sqrt(2/L)*Math.sin((Math.PI*x5[i])/L), 2);
        }
        var data6 = source6.data
        var av = data6['x']
        for (var i = 0; i < av.length; i++) {
            av[i] = L*Math.sqrt(1/12 - 1/(2*Math.pow(Math.PI, 2)))
        }
        var data7 = source7.data
        var x_av = data7['x']
        for (var i = 0; i < x_av.length; i++) {
            x_av[i] = L/2
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
    x_wave, av_wave, E_list, phi_wave, prob_wave = generate_wavedata()
    n_plot = generate_n_plot(x_wave, av_wave, E_list[0], phi_wave, prob_wave)
    L_plot = generate_L_plot(E_list)
    n_slider, L_slider = generate_callbacks(
        x_wave, av_wave, phi_wave, prob_wave, E_list)
    layout = row(n_plot, L_plot, widgetbox(n_slider, L_slider))

    show(layout)


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    return_graphics()
