import numpy as np
import plotly.graph_objects as go

from gravity.gravity_simulator import GravitySimulator


def create_figure(simulator: GravitySimulator):
    color = "#b4b4b4"
    sizes = 8 + np.log(simulator.m * 10)
    title = f"Time: {round(sum(simulator.sleep_time_history) * simulator.time_speed)}"

    fig = go.Figure()

    if simulator.show_points:
        fig.add_trace(go.Scatter(x=simulator.x, y=simulator.y, mode='markers',
                                 marker=dict(size=sizes, color=color))
                      )

    if simulator.show_field:
        length = 100

        fig.add_trace(go.Heatmap(z=simulator.gravitational_field,
                                 x=np.linspace(-1, 1, length), y=np.linspace(-1, 1, length),
                                 colorscale='jet', opacity=0.3, showscale=False))

    if simulator.show_trace:
        trace_length = 15
        for i in range(1, trace_length):
            try:
                x_trace = simulator.x_history[-i]
                y_trace = simulator.y_history[-i]
            except IndexError:
                x_trace = None
                y_trace = None

            fig.add_trace(go.Scatter(x=x_trace, y=y_trace, mode='markers',
                                     marker=dict(size=sizes*0.8, color=color,
                                                 opacity=(trace_length - i)/trace_length))
                          )

    scale = 1.1
    fig.update_layout(xaxis=dict(range=[-1*scale, 1*scale]),
                      yaxis=dict(range=[-1*scale, 1*scale], showgrid=False, zeroline=False),
                      autosize=False, width=600, height=700, title_text=title, title_x=0.5,
                      showlegend=False,
                      )
    fig.update_layout(
        shapes=[
            go.layout.Shape(type='rect', xref='paper', yref='paper', x0=0, y0=0, x1=1, y1=1,
                            line=dict(color='white', width=2), fillcolor='rgba(255, 255, 255, 0)')
        ]
    )

    return fig


def animate_points(chart_placeholder, simulator: GravitySimulator):
    while True:
        simulator.simulate_one_iteration()
        fig = create_figure(simulator)
        chart_placeholder.plotly_chart(fig, use_container_width=False, clear_on_update=False)

        if np.all((simulator.x > 1) | (simulator.x < -1) | (simulator.y > 1) | (simulator.y < -1)):
            break
