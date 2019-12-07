import pandas as pd
import numpy as np
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
from sklearn import svm


def save_corr_matrix(df, file_name):
    corrs = df.corr().fillna(0)
    fig = go.Figure(data=go.Heatmap(z=corrs.values, x=list(corrs.columns), y=list(corrs.index)))
    fig.update_layout(title="Матрица корреляции")
    fig.write_html(file_name, auto_open=True)


def signs_df(df, signs_df_mas):
    signs_df = []
    corrs = df.corr().fillna(0)
    for elem in signs_df_mas:
        d = dict()
        d["skill1"] = elem[0]
        d["skill2"] = elem[1]
        d["value"] = corrs[elem[0]][elem[1]]
        signs_df.append(d)
    return pd.DataFrame(signs_df)


def save_line(df, file_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["skill1"], y=df["value"], text=df["skill2"], mode="lines+markers+text"))
    fig.update_layout(title="Линейная зависимость")
    fig.write_html(file_name, auto_open=True)


def save_bar(df, file_name):
    trace = go.Bar(
        x=df["skill1"],
        y=df["value"],
        text=df["skill2"],
        textposition='auto'
    )
    fig = go.Figure(data=trace, layout=go.Layout(barmode='stack'))
    fig.update_layout(title="Гистограма")
    fig.write_html(file_name, auto_open=True)


def save_scatter_matrix(df, file_name):
    fig = go.Figure(data=go.Splom(
        dimensions=[dict(label='skill1',
                         values=df['skill1']),
                    dict(label='skill2',
                         values=df['skill2']),
                    dict(label='value',
                         values=df['value'])],
        text=df['skill2'],
    ))
    fig.update_layout(title="Матрица рассеяния")
    fig.write_html(file_name, auto_open=True)


def save_word_cloud(df, file_name):
    text = ""
    for skills in df["key_skills"].values:
        for el in skills.split(';'):
            #if el.find('1c') != -1 or el.find('1с') != -1:
            #    text += "1C:предприятие" + ' '
            #else:
            text += el + ' '
    wordcloud = WordCloud(
        width=3000,
        height=2000,
        background_color='black').generate(str(text))
    wordcloud.to_file(file_name)


def save_outbursts_diagram(df, file_name):
    trace1 = df["min_salary"]
    trace2 = df["max_salary"]
    fig = go.Figure()
    fig.add_trace(go.Box(y=trace1, name='min salary', marker_color='darkblue'))
    fig.add_trace(go.Box(y=trace2, name='max salary', marker_color='lightseagreen'))
    fig.update_layout(title="Диаграмма размаха выбросов")
    fig.write_html(file_name, auto_open=True)


def find_outbursts(df, column):
    return df[np.abs(df[column] - df[column].mean()) > (3 * df[column].std())]


def print_outbursts(df):
    print(len(find_outbursts(df, "min_salary")))
    print(len(find_outbursts(df, "max_salary")))


def change_outbursts(df, column):
    outbursts = find_outbursts(df, column)
    mean = round(df[column].mean(), 0)
    std = round(df[column].std(), 0)
    for elem in outbursts["id"]:
        df.update(df[df["id"] == elem][column].apply(lambda x: mean - 3*std if (x-mean < 0) else mean + 3*std))
    return df


def delete_outbursts(df, column):
    outbursts = find_outbursts(df, column)
    for elem in outbursts["id"]:
        df = df[df["id"] != elem]
    return df