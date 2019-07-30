import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class Dashapp:


    @staticmethod
    def Draw_all(ls_result,strkey):
        df=ls_result
        app.layout = html.Div([
            dcc.Graph(
                id='Employees_infor',
                figure={
                    'data': [
                        go.Scatter(
                            x=df[i][df[strkey]],
                            text=df[i][strkey],
                            mode='lines+markers',
                            opacity=0.7,
                            marker={
                                'size': 15,
                                'line': {'width': 0.5, 'color': 'white'}
                            },
                            lines={
                                'line':{'with':0.5,'color':'red'}
                            }
                            name=i
                        ) for i in len(ls_result)
                    ],
                    'layout': go.Layout(
                        xaxis={'type': 'log', 'title': strkey},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )
        ])

        if __name__ == '__main__':
            app.run_server(debug=True)