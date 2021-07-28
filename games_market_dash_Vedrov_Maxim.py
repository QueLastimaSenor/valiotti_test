import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

#Отбрасываем данные с Null и старше 2000 года
df = (pd.read_csv('games.csv')).dropna()
df = df[df['Year_of_Release'] >= 2000]

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                update_title=None)


app.layout = dbc.Container([

    html.P(children='Select range', style={'margin-top': '10px'}),
    dcc.RangeSlider(
        id='slider',
        min=min(df['Year_of_Release']),
        max=max(df['Year_of_Release']),
        step=None,
        marks={
            int(x): x for x in df['Year_of_Release'].unique()
        },
        value=[2002,2014],
        tooltip={'always visible':False,  # show current slider values
            'placement':'bottom'},
    ),

    html.P(children='Select genre', style={'margin-top': '10px'}),
    dcc.Dropdown(
        id='dropdown_genre',
        multi=True,
        options=[{
            'label': x,
            'value': x
        } for x in sorted(df['Genre'].unique())],
        value=['Sports', 'Adventure']
    ),

    html.P(children='Select rating', style={'margin-top': '10px'}),
    dcc.Dropdown(
        id='dropdown_rating',
        multi=True,
        options=[{
            'label': x,
            'value': x
        } for x in sorted(df['Rating'].unique())],
        value=['E', 'E10+']
    ),

    html.H4(id='games', style={'margin-top': '10px'}),     

    dbc.Row([

        dbc.Col([
            dcc.Graph(
                    id='area_stacked',
                    ),
        ], width=6),
        
        dbc.Col([
            dcc.Graph(
                    id='scatter_genres',
                    ),
        ], width=6),

    ], justify='center')

], fluid=True)

@app.callback(
    Output(component_id='area_stacked', component_property='figure'),
    [Input(component_id='dropdown_genre', component_property='value'),
     Input(component_id='dropdown_rating', component_property='value'),
     Input(component_id='slider', component_property='value')]
)
def update_area_plot(val_genre, val_rating, val_slider):
    #Выборка данных
    df_sample = df[(df['Genre'].isin(val_genre)) &
                    (df['Rating'].isin(val_rating))]
    #Агрегация данных                   
    df_year = df_sample.groupby(['Year_of_Release', 'Platform']).agg({'Platform': ['count']}).reset_index()     
    df_year.columns = ['Year_of_Release', 'Platform', 'Count']
    
    df_area = df_year[(df_year['Year_of_Release'] < val_slider[1])
                    & (df_year['Year_of_Release'] > val_slider[0])]
    
    #Построение графиков
    fig_stacked = px.area(df_area, x='Year_of_Release', y='Count', 
                      line_group='Platform', color='Platform')
    fig_stacked.update_layout(
        title='Stacked area plot',
        xaxis_title='Year_of_Release',
        yaxis_title='Number of games'      
    )

    return fig_stacked

@app.callback(
    [Output(component_id='scatter_genres', component_property='figure'),
     Output(component_id='games', component_property='children')],
    [Input(component_id='dropdown_genre', component_property='value'),
     Input(component_id='dropdown_rating', component_property='value'),
     Input(component_id='slider', component_property='value')]
)
def update_scatter_genre(val_genre, val_rating, val_slider):
    #Выборка данных
    df_prep = df[(df['Genre'].isin(val_genre))
            & ((df['Rating'].isin(val_rating)))
            & (df['Year_of_Release'] < val_slider[1])
            & (df['Year_of_Release'] > val_slider[0])]
    #Отбрасываем рэйтинг с ожиданием оценки
    df_sc = df_prep[df_prep['User_Score'] != 'tbd']
    
    #Построение графиков
    fig_sc = px.scatter(x=sorted(df_sc['User_Score']), 
                        y=df_sc['Critic_Score'], 
                        color=df_sc['Genre'])
    fig_sc.update_layout(
        title='Scatter plot',
        xaxis_title='Users Score',
        yaxis_title='Critics Score'
    )
     
    #Кол-во выбранных игр
    count_games = df_prep['Name'].count()

    return fig_sc, f'Total number of games: {count_games}'


if __name__ == '__main__':
    app.run_server()