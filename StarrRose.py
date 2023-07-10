from PIL import Image, ImageDraw
import math

import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# now gonna turn this into a dash app
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
    
    # the starr rose is a modification of the maurer rose:
    # firstly, whereas the maurer rose has radial function r = sin(a*theta), the starr rose has r = 2 + 1/2sin(a*t) 
    # where a is a fixed parameter and t is a variable angle parameter
    # this means the radius oscillates between 3/2 and 5/2 instead of 0 and 1
    # the angular function is stranger though as it is parameterised by t to generate "backward" movement
    # we have theta(t) = t + sin(b*t)/c where b,c are fixed parameters
    # the full parameterised function is (x(t),y(t)) = r(t) * (cos(theta(t), sin(theta(t))) 

    image = Image.new("RGB", (width, height), "white")

    draw = ImageDraw.Draw(image)
    points = []

    loops = 50

    for k in range(loops):

        #scale = 1 - ((k+1)/loops)**2
        scale = (k+1)/loops

        for i in range(max):
            # find our angle parameter t in radians
            t = (2*math.pi * i) / max

            r = 2 + 0.5 * math.sin(a*t)

            theta = t + math.sin(b*t)/c

            xcoord = r * math.cos(theta)
            ycoord = r * math.sin(theta)
            #now we need to translate these points so the rose is centered (and optionally scale them so we can see it)
            points.append((width/2 + scale*petal_size*xcoord, height/2 + scale*petal_size*ycoord))
        
        draw.line(points, width=1, fill="black", joint="curve")
        points = []
    

    # convert image to a px figure for display purposes
    fig = px.imshow(image)
    fig.update_layout(width=1200, height=1200)
    fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
