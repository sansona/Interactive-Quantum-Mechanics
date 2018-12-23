import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import CustomJS, Slider
from bokeh.plotting import figure, output_file, show, ColumnDataSource

L = 1  # if change this, need to reflect in JS code to reflct. See line 24
x = np.linspace(0, L, 1000)
phi = np.sqrt(2/L)*np.sin((np.pi*x)/L)
prob_density = phi**2

phi_source = ColumnDataSource(data=dict(x=x, y=phi))
prob_source = ColumnDataSource(data=dict(x=x, y=prob_density))

# -----------------------------------------------------------------------------


def generate_plot_obj(phi_col=phi_source, prob_col=prob_source, size=750):
    plot = figure(y_range=(-3, 3), plot_width=750, plot_height=750)
    plot.xaxis.axis_label = 'x'
    plot.xaxis.axis_label_text_font_size = '24pt'
    plot.line('x', 'y', source=phi_col, line_width=6,
              line_alpha=0.6, legend='Phi')
    plot.line('x', 'y', source=prob_col,
              color='red', line_width=6, line_alpha=0.6,
              legend='Probability density')
    plot.legend.location = 'top_left'
    plot.legend.click_policy = 'hide'

    return plot

# -----------------------------------------------------------------------------


def generate_n_callback(phi_col=phi_source, prob_col=prob_source):
    n_callback = CustomJS(args=dict(
        source=phi_source, source2=prob_source),
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
		source.change.emit();
	""")

    slider = Slider(start=1, end=100, value=1, step=1,
                    title='n', callback=n_callback)

    return slider


if __name__ == '__main__':
    plot = generate_plot_obj()
    n_slider = generate_n_callback()
    layout = row(plot, widgetbox(n_slider))
    show(layout)
