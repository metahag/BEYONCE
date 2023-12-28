import dash
from dfply import *
import pandas as pd 
import glob2 as glob
import chart_studio.plotly as py
from plotly.graph_objs import *
import plotly.io as pio
import plotly.express as px
import os
from pathlib import Path

file_path = Path("assets/renaissance.css")

data_dir = "csv_files"
joined_files = os.path.join(f"{data_dir}/*.csv") 
  
joined_list = glob.glob(joined_files) 
  
df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True) 
df.columns=df.columns.str.lower().str.replace(' ','_')
print(df) 

pio.templates.default = "plotly_dark"
color_discrete_map= {'Won': "#A9ACB6",
                     'Nominated': "#A9ACB6",
                     'Runner-Up': "#A9ACB6",
                     "Bronze": "#A9ACB6",
                     'Eliminated': "#A9ACB6",
                     'Pending': "#A9ACB6"}


# start of the app
app = dash.Dash(__name__, external_stylesheets=[file_path])

# first figure number of won awards
fig = (df >> select(X.award_category, X.result) >> group_by(X.result) >> summarize(awards=n_distinct(X.award_category)))
fig = (pd.DataFrame(fig) >> arrange(X.awards, ascending = False))
print(fig)
fig = px.bar(fig, x="result", y="awards", color="result", color_discrete_map=color_discrete_map)
fig = fig.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title = "10,10,10 Across the Board",
                        xaxis=dict(title='Results'), yaxis=dict(title='Amount'))

# second figure parallel categories
fig_par = (df >> select(X.album, X.main_artist, X.year, X.us, X.uk))
fig_par = pd.DataFrame(fig_par)
fig_par = px.parallel_categories(fig_par, color="year")
fig_par = fig_par.update_layout(coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title = "I'm One of One, I'm Number One")


# third figure pie chart
fig_pie = (df >> select(X.country) >> mutate(performance= n_distinct(X.country)))
fig_pie = (pd.DataFrame(fig_pie))
fig_pie = fig_pie.dropna()
fig_pie = px.pie(fig_pie, values='performance', names='country', color_discrete_sequence=px.colors.sequential.Greys)
fig_pie = fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title = "America has a Problem")

# ui
app.layout = dash.html.Div([
    dash.html.Div(
        className="h1",
        children=[
            dash.html.Div('Welcome to the Renaissance')
        ]
    ),
    dash.html.Div(
        children=[
            dash.html.Div(
                children=[dash.dcc.Graph(id='album-charts', figure=fig_par)],
                style={'width':'80%', 'grid-area': 'upper-left', 'padding-left':'10%'}
            ),
            dash.html.Div(
                children=[dash.dcc.Graph(id='awards-won', figure=fig)],
                style={'width':'60%', 'grid-area': 'lower-left'}
            ),
            dash.html.Div(
                children=[dash.dcc.Graph(id='performances', figure=fig_pie)],
                style={'width':'50%', 'grid-area': 'upper-right', 'padding-left':'50%'}
            ),
        ],
        style={
            'display': 'grid',
            'grid-template-columns': '1fr 1fr',
            'grid-template-rows': '1fr 1fr',
            'grid-template-areas': '"upper-left upper-right" "lower-left ."',
            'height': '100vh'
        }
    )
])



# run app
if __name__ == '__main__':
    app.run(debug=True)