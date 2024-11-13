from dash import Dash, dcc, html
import pandas as pd
from dash.dependencies import Output, Input

# Load and process your data
data = pd.read_csv("sampledata.csv")
data["timestamp"] = pd.to_datetime(data["timestamp"], format="%Y-%m-%d %H:%M:%S")
data.sort_values("timestamp", inplace=True)

# External stylesheet for the app
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Website Analytics: A Dash Demo App!"

# Define the layout of the app
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📈", className="header-emoji"),
                html.H1(children="Website Analytics", className="header-title"),
                html.P(
                    children="Analyze the performance of a simulated social media website",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.P("Select Metrics to Display:"),
                dcc.Checklist(
                    id="metrics-checklist",
                    options=[
                        {"label": "Page Load Time (ms)", "value": "page_load_time(ms)"},
                        {"label": "Requests per Second", "value": "requests_per_second"},
                        {"label": "Server Response Time (ms)", "value": "server_response_time(ms)"},
                        {"label": "Active Users", "value": "active_users"},
                        {"label": "Error Rate (%)", "value": "error_rate(%)"},
                    ],
                    value=["page_load_time(ms)", "requests_per_second", "server_response_time(ms)", "active_users", "error_rate(%)"],  # Default selection
                ),
            ],
            className="menu",
        ),
        dcc.Graph(id="combined-graph"),
    ]
)

# Callback to update the graph based on the selected metrics
@app.callback(
    Output("combined-graph", "figure"),
    [Input("metrics-checklist", "value")]
)
def update_graph(selected_metrics):
    # Initialize an empty list to hold the traces
    traces = []

    # Normalize each dataset to be in the range [0, 1] for selected metrics
    if "page_load_time(ms)" in selected_metrics:
        normalized_page_load_time = data["page_load_time(ms)"] / data["page_load_time(ms)"].max()
        traces.append({
            "x": data["timestamp"],
            "y": normalized_page_load_time,
            "type": "line",
            "name": "Page Load Time (ms) (Normalized)",
        })
    
    if "requests_per_second" in selected_metrics:
        normalized_requests_per_second = data["requests_per_second"] / data["requests_per_second"].max()
        traces.append({
            "x": data["timestamp"],
            "y": normalized_requests_per_second,
            "type": "line",
            "name": "Requests per Second (Normalized)",
        })
    
    if "server_response_time(ms)" in selected_metrics:
        normalized_server_response_time = data["server_response_time(ms)"] / data["server_response_time(ms)"].max()
        traces.append({
            "x": data["timestamp"],
            "y": normalized_server_response_time,
            "type": "line",
            "name": "Server Response Time (ms) (Normalized)",
        })
    
    if "active_users" in selected_metrics:
        normalized_active_users = data["active_users"] / data["active_users"].max()
        traces.append({
            "x": data["timestamp"],
            "y": normalized_active_users,
            "type": "line",
            "name": "Active Users (Normalized)",
        })
    
    if "error_rate(%)" in selected_metrics:
        normalized_error_rate = data["error_rate(%)"] / data["error_rate(%)"].max()
        traces.append({
            "x": data["timestamp"],
            "y": normalized_error_rate,
            "type": "line",
            "name": "Error Rate (%) (Normalized)",
        })

    # Create the figure with all selected traces
    figure = {
        "data": traces,
        "layout": {
            "title": "Website Analytics Over Time (Normalized)",
            "xaxis": {"title": "Timestamp"},
            "yaxis": {"title": "Normalized Value"},
            "showlegend": True,  # Show legend for trace names
        },
    }

    return figure

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
