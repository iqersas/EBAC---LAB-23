import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv("ecommerce_estatistica.csv")

app = dash.Dash(__name__)
app.title = "Dashboard E-commerce"

app.layout = html.Div(
    [
        html.H1("Dashboard E-commerce", style={"textAlign": "center"}),
        html.Label("Selecione o gráfico:"),
        dcc.Dropdown(
            id="grafico_dropdown",
            options=[
                {
                    "label": "Preço vs Qtd Vendidos",
                    "value": "preco_vendidos",
                },
                {"label": "Média de Preço por Marca", "value": "preco_marca"},
                {
                    "label": "Distribuição de Notas por Material",
                    "value": "nota_material",
                },
                {
                    "label": "Distribuição das Vendas por Marca",
                    "value": "vendas_marca",
                },
            ],
            value="preco_vendidos",
        ),
        dcc.Graph(id="grafico_output"),
    ]
)


@app.callback(Output("grafico_output", "figure"), Input("grafico_dropdown", "value"))
def atualizar_grafico(tipo):
    if tipo == "preco_vendidos":
        fig = px.scatter(
            df, x="Preço", y="Qtd_Vendidos", title="Preço vs Quantidade Vendida"
        )
    elif tipo == "preco_marca":
        df_agg = df.groupby("Marca")["Preço"].mean().reset_index()
        df_agg = df_agg.sort_values("Preço", ascending=False).head(10)
        fig = px.bar(
            df_agg,
            x="Marca",
            y="Preço",
            title="Top 10 Marcas com Maior Preço Médio",
        )
    elif tipo == "nota_material":
        fig = px.box(
            df, x="Material", y="Nota", title="Distribuição de Notas por Material"
        )
    elif tipo == "vendas_marca":
        df_agg = df.groupby("Marca")["Qtd_Vendidos"].sum().reset_index()
        fig = px.pie(
            df_agg,
            names="Marca",
            values="Qtd_Vendidos",
            title="Distribuição das Vendas por Marca",
        )
    else:
        fig = px.scatter(title="Gráfico não encontrado")
    return fig


if __name__ == "__main__":
    app.run(debug=True)
