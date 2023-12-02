import plotly.graph_objects as go
import numpy as np
import time


center_x, center_y = 0, 0
num_frames = 50

x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(x, y)
Z = np.zeros(X.shape)

x1, y1 = center_x - 1, center_y - 1
x2, y2 = center_x + 1, center_y + 1


def create_figure(x_vector, y_vector):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_vector,
        y=y_vector,
        mode='markers',
        marker=dict(size=10, color='red'),
    ))

    fig.update_xaxes(showticklabels=True)
    fig.update_yaxes(showticklabels=True)

    # fig.layout.yaxis.scaleanchor = "x"

    fig.update_layout(xaxis=dict(range=[-1, 1]),
                      yaxis=dict(range=[-1, 1], showgrid=False, zeroline=False),
                      autosize=False,
                      width=600*1.1,
                      height=700*1.1,
                      )

    # fig.update_yaxes(
    #     scaleanchor="x",
    #     scaleratio=1,
    # )


    fig.update_layout(
        shapes=[
            go.layout.Shape(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color='white', width=2),
                fillcolor='rgba(255, 255, 255, 0)'  # Set fill color to transparent
            )
        ]
    )

    return fig


def animate_points(chart_placeholder, x_start_positions, y_start_positions, mass_values):
    x_vector, y_vector = x_start_positions, y_start_positions
    for i in range(num_frames):
        time.sleep(0.2)

        x_vector = x_vector + 0.01*np.random.normal(size=len(x_vector))
        y_vector = y_vector + 0.01*np.random.normal(size=len(y_vector))

        fig = create_figure(x_vector, y_vector)
        chart_placeholder.plotly_chart(fig, use_container_width=False, clear_on_update=True)
