import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


mapbox_access_token = '*'

traces_df = pd.DataFrame([[1, 1, 37.5373359, 127.0073906, '한남더힐'],
                         [1, 2, 37.4703527, 127.0358695, '양재시민의숲역'],
                         [1, 3, 37.3925707, 127.109807, '판교 현대백화점'],
                         [2, 1, 33.5104135, 126.4891647, '제주공항'],
                         [2, 2, 37.2675123, 126.9993292, '수원역']],
                         columns=['id', 'trace_num', 'lat', 'lon', 'trace_name'])

traces_df['text_label'] = traces_df['id'].astype('str') + '번째 확진자 동선 ' + traces_df['trace_num'].astype('str') + ' : ' + traces_df['trace_name']


def generate_traces(traces_df):
    traces = []
    users = traces_df.id.unique()
    for user_id in users:
        trace = dict(
            type='scattermapbox',
            mode='markers+lines',
            hoverinfo="text",
            lat=traces_df[traces_df.id == user_id].lat,
            lon=traces_df[traces_df.id == user_id].lon,
            text=traces_df[traces_df.id == user_id].text_label,
            marker=dict(
                size=10
            ),
            name=f'{user_id}번째 확진자'
        )
        traces.append(trace)
    return traces


def generate_table(df, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +
        # Body
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(min(len(df), max_rows))]
    )


mapbox_layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(
        l=30,
        r=30,
        b=20,
        t=40
    ),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation='h'),
    title='신종 코로나 확진자 동선 지도',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        # style="light",
        style="mapbox://styles/mint-choc/ck64zg4kn13uu1inwzj3957w6",
        center=dict(
            lat=37.47,
            lon=127.03
        ),
        zoom=7,
    )
)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H4(children='Corona Virus by any-project'),
    dcc.Graph(
        figure=dict(
            data=generate_traces(traces_df),
            layout=mapbox_layout
        ),
        id='map',
        style={'height': 500}
    ),
    generate_table(traces_df),
    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                       350, 430, 474, 526, 488, 537, 500, 439],
                    name='China',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                       299, 340, 403, 549, 499],
                    name='Rest of world',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='신종 코로나 확진자/사망자/퇴원자 추이 그래프',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
