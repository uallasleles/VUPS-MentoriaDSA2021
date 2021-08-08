import dash_html_components as html
import dash_bootstrap_components as dbc


card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "Aqui pode ficar um KPI.",
                className="card-text",
            ),
        ]
    ),
]

# KPIs
def widget_kpis():
    dbc =   dbc.Container(
                return  html.Div(
                            [
                                dbc.Row([
                                    dbc.Col(dbc.Card(card_content, color="light"), width=6, lg=3),
                                    dbc.Col(dbc.Card(card_content, color="dark", inverse=True), width=6, lg=3),
                                    dbc.Col(dbc.Card(card_content, color="info", inverse=True), width=6, lg=3),
                                    dbc.Col(dbc.Card(card_content, color="success", inverse=True), width=6, lg=3),]
                                )
                            ])
            )