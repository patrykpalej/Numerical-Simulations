import time
import plotly.graph_objects as go


def create_figure(simulator, title):
    fig = go.Figure()

    # Humans
    fig.add_trace(go.Scatter(x=[human.x for human in simulator.humans],
                             y=[human.y for human in simulator.humans], mode='markers',
                             marker=dict(size=10, color='orange'))
                  )

    # Zombies
    fig.add_trace(go.Scatter(x=[zombie.x for zombie in simulator.zombies],
                             y=[zombie.y for zombie in simulator.zombies], mode='markers',
                             marker=dict(size=10, color='green'))
                  )

    fig.update_layout(xaxis=dict(range=[0, 100]),
                      yaxis=dict(range=[0, 100], showgrid=False, zeroline=False),
                      autosize=False, width=550, height=650, title_text=title, title_x=0.45,
                      showlegend=False,
                      )

    fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, line=dict(color="White"),
                  fillcolor="rgba(255,255,255,0)")

    return fig


def animate_points(chart_placeholder, simulator):
    while True:
        simulator.run_single_iteration()
        simulator.t += 1

        time_to_sleep = 1 / simulator.simulation_speed * 10
        time.sleep(time_to_sleep)

        if not simulator.humans and not simulator.zombies:
            title = "All died"
        elif not simulator.humans:
            title = "Zombies won"
        elif not simulator.zombies:
            title = "Humans won"
        else:
            title = f"Time: {simulator.t}"

        fig = create_figure(simulator, title)
        chart_placeholder.plotly_chart(fig, use_container_width=False, clear_on_update=False)

        if not simulator.humans or not simulator.zombies:
            break
