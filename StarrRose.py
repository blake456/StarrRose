from PIL import Image, ImageDraw
import math

import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Generating Roses', style = {"text-align": "center"}),

    html.Div(
        children = [
            dcc.Slider(
                0,20,1,
                value = 8,
                id = 'a'
            )
        ],
        style=dict(width='33%')
    ),
    html.Div(
        children = [
            dcc.Slider(
                0,20,1,
                value = 16,
                id = 'b'
            )
        ],
        style=dict(width='33%')
    ),
    html.Div(
        children = [
            dcc.Slider(
                0,20,1,
                value = 16,
                id = 'c'
            )
        ],
        style=dict(width='33%')
    ),

    html.Hr(),

    dcc.Graph(id='Starr_Rose', figure = {})

])

@app.callback(
    Output('Starr_Rose', 'figure'),
    Input('a','value'),
    Input('b','value'),
    Input('c','value')
)
def StarrRose(a,b,c):
    height = 1200
    width = height
    petal_size = 0.3*width/2
    max = 1000
    
    image = Image.new("RGB", (width, height), "white")

    draw = ImageDraw.Draw(image)
    points = []

    loops = 50
    for k in range(loops):
        scale = (k+1)/loops

        for i in range(max):
            # find our angle parameter t in radians
            t = (2*math.pi * i) / max

            # work out polar coordinate values
            r = 2 + 0.5 * math.sin(a*t)
            theta = t + math.sin(b*t)/c

            # convert polar coordinate values to cartesian values
            xcoord = r * math.cos(theta)
            ycoord = r * math.sin(theta)
            
            # translate and scale these points so the rose is centered and of a reasonable size
            points.append((width/2 + scale*petal_size*xcoord, height/2 + scale*petal_size*ycoord))

        # draw this loop, then clesr points for the next loop
        draw.line(points, width=1, fill="black", joint="curve")
        points = []
    
    # convert image to a px figure to display it
    fig = px.imshow(image)
    fig.update_layout(width=1200, height=1200)
    fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
