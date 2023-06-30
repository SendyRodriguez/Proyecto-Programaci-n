import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
st.set_page_config(page_title="Dashboard", layout='wide',
                   initial_sidebar_state='auto')
st.title('POSITIVOS COVID-19 - 2023')
data = pd.read_csv("positivos_covid_2023.csv")
data["FECHA_RESULTADO"] = data["FECHA_RESULTADO"].astype(
    str).str.replace(",", "").str.split(".", expand=True)[0]
data["FECHA_RESULTADO"] = pd.to_datetime(
    data["FECHA_RESULTADO"], format="%Y%m%d", errors='coerce').dt.strftime("%Y%m%d")
num_filas = len(data)-1
year_filter_options = [2023]
year_filter = st.sidebar.radio("Filtrar por año", year_filter_options)
filtrado = data[data["FECHA_RESULTADO"].str.startswith(str(year_filter))]
porcentaje_total = (num_filas / num_filas) * 100
fig = go.Figure()
fig.add_trace(go.Bar(
    y=["Total de registros: "+str(num_filas)],
    x=[porcentaje_total],
    orientation='h',
    marker=dict(
        color=['#1f77b4']
    ),
    text=[f"{porcentaje_total:.2f}%"],
    textposition="inside"
))
fig.update_layout(
    title="Total de positivos covid: "+str(num_filas),
    xaxis_title="Porcentaje",
    yaxis_title="",
    showlegend=False
)
st.plotly_chart(fig)
count_by_department = filtrado["DEPARTAMENTO"].value_counts().reset_index()
count_by_department.columns = ["Departamento", "Total"]
colors = px.colors.qualitative.Plotly
fig = px.bar(count_by_department, x="Departamento", y="Total",
             title="Positivos COVID-19 por DEPARTAMENTO - 2023", color="Departamento", color_discrete_sequence=colors)
st.plotly_chart(fig)
departamentos = filtrado['DEPARTAMENTO'].unique()
distritos = filtrado['DISTRITO'].unique()
departamentos = list(departamentos)
departamentos.sort()
departamento = st.sidebar.selectbox('Seleccionar departamento', departamentos)
filtrado = filtrado[filtrado['DEPARTAMENTO'] == departamento]
if departamento:
    provincias = filtrado['PROVINCIA'].unique()
    provincias = list(provincias)
    provincias.sort()
    provincia = st.sidebar.selectbox('Seleccionar provincia', provincias)
    if provincia:
        filtrado = filtrado[filtrado['PROVINCIA'] == provincia]
        distritos = filtrado['DISTRITO'].unique()
        distritos = list(distritos)
        distritos.sort()
        distrito = st.sidebar.selectbox('Seleccionar distrito', distritos)
        if distrito:
            filtrado = filtrado[filtrado['DISTRITO'] == distrito]
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
filtrado['FECHA_RESULTADO'] = pd.to_datetime(
    filtrado['FECHA_RESULTADO'], format='%Y%m%d')
filtrado['MES'] = filtrado['FECHA_RESULTADO'].dt.month
meses_unicos = filtrado['MES'].unique()
meses_unicos.sort()
meses_filtrados = [meses[mes - 1] for mes in meses_unicos]
mes_seleccionado = st.sidebar.selectbox('Seleccionar mes', meses_filtrados)
num_filas_filtrado = 0
if mes_seleccionado:
    mes_numero = meses_unicos[meses_filtrados.index(mes_seleccionado)]
    filtrado = filtrado[filtrado['MES'] == mes_numero]
    num_filas_filtrado = len(filtrado) - 1
count_by_department = filtrado['DEPARTAMENTO'].value_counts().reset_index()
count_by_department.columns = ['Departamento', 'Total']
count_by_province = filtrado['PROVINCIA'].value_counts().reset_index()
count_by_province.columns = ['Provincia', 'Total']
count_by_district = filtrado['DISTRITO'].value_counts().reset_index()
count_by_district.columns = ['Distrito', 'Total']
fig = sp.make_subplots(rows=1, cols=3)
fig.add_trace(go.Bar(x=count_by_department['Departamento'],
              y=count_by_department['Total'], name='Departamento'), row=1, col=1)
fig.add_trace(go.Bar(x=count_by_province['Provincia'],
              y=count_by_province['Total'], name='Provincia'), row=1, col=2)
fig.add_trace(go.Bar(x=count_by_district['Distrito'],
              y=count_by_district['Total'], name='Distrito'), row=1, col=3)
fig.update_layout(title='Conteos por Ubicación', showlegend=False)
fig.update_layout(title='Conteo por DEPARTAMENTO, PROVINCIA y DISTRITO durante el mes de '+str(mes_seleccionado),
                  xaxis_title='Categoría', yaxis_title='Total',
                  showlegend=True)
st.plotly_chart(fig)
count_by_method = filtrado["METODODX"].value_counts().reset_index()
count_by_method.columns = ["Metodo", "Total"]
count_by_method = count_by_method[count_by_method["Metodo"].isin([
                                                                 "AG", "PCR", "PR"])]
fig = px.bar(count_by_method, x="Metodo", y="Total", title="Tipo de MÉTODO durante el mes de " +
             str(mes_seleccionado), color="Metodo", color_discrete_sequence=px.colors.qualitative.Plotly)
st.plotly_chart(fig)
count_by_sex = filtrado["SEXO"].value_counts().reset_index()
count_by_sex.columns = ["Sexo", "Total"]
fig = px.pie(count_by_sex, values="Total", names="Sexo",
             title="Total por SEXO durante el mes de "+str(mes_seleccionado))
st.plotly_chart(fig)
if len(filtrado) > 0:
    conteo_edad = filtrado['EDAD'].value_counts().reset_index()
    conteo_edad.columns = ['EDAD', 'TOTAL']
    fig = go.Figure(
        data=[go.Pie(labels=conteo_edad['EDAD'], values=conteo_edad['TOTAL'])])
    fig.update_traces(textinfo='percent+label', textposition='outside',
                      pull=[0.1] * len(conteo_edad))
    fig.update_layout(
        title="Total según EDAD",
        xaxis_title="Porcentaje",
        yaxis_title="",
        showlegend=True
    )
    st.plotly_chart(fig)
    st.subheader('TABLA POSITIVOS COVID-19')
    columnas = ['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO', 'SEXO', 'EDAD']
    st.write(filtrado[columnas])
    st.balloons()
else:
    st.write('No hay datos para mostrar.')
