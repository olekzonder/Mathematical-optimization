import streamlit as st

from point import Point, Points
from graph import plot_graph
from opt import filter_optimal, Hermeyer, ideal_point, Linear, Threshold

def generate_points(n):
    st.session_state.points = Points()
    st.session_state.points.generate(n)
    return st.session_state.points

def get_points():
    return st.session_state.points

st.set_page_config(
    page_title="ФММРАЗ",
    page_icon="🤠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Выполнил Александр Смирнов",
        'Get help': "https://github.com/olekzonder"
    }
)
methods = ['Генерация нового графика', 'Нахождение множества Парето', 
           'Метод обобщённой функции (линейная свёртка)', 
           'Метод обобщённой функции (функция Гермейера)', 
           'Метод пороговой оптимизации', 'Метод идеальной точки']
st.sidebar.write("# Нахождение оптимального по Парето проекта")
st.sidebar.write("КДЗ 1.6")
method = st.sidebar.selectbox('## Выберите пункт меню:', methods)

@st.cache_data
def calculate_w2(w1):
    return 1.0 - w1
match(method):
    case 'Генерация нового графика':
        n = st.sidebar.slider('Выберите количество точек', 10, 1000, 100)
        points  = generate_points(n)
        fig = plot_graph(points=points.points)

    case 'Нахождение множества Парето':
        points = get_points()
        unopt,pareto = filter_optimal(points.points)
        fig = plot_graph(unopt=unopt,pareto=pareto)
    
    case 'Метод обобщённой функции (линейная свёртка)':
        points = get_points()
        unopt,pareto = filter_optimal(points.points)
        w1 = st.sidebar.slider('Выберите вес первого критерия', 0.0, 1.0, 0.1)
        w2 = calculate_w2(w1)
        st.sidebar.slider("Вес второго критерия",0.0,1.0,w2)
        unopt,pareto,optimal = Linear(w1,w2).linear_optimal(unopt,pareto)
        fig = plot_graph(unopt=unopt,pareto=pareto,optimal=optimal)

    case 'Метод обобщённой функции (функция Гермейера)':
        points = get_points()
        unopt,pareto = filter_optimal(points.points)
        unopt,pareto,optimal = Hermeyer().hermeyer_optimal(unopt,pareto)
        fig = plot_graph(unopt=unopt,pareto=pareto,optimal=optimal)

    case 'Метод пороговой оптимизации':
        points = get_points()
        unopt,pareto = filter_optimal(points.points)
        criterion = st.sidebar.selectbox("Выберите главный критерий",['f1','f2'])
        if criterion == 'f1':
            threshold = st.sidebar.slider('Выберите γ2',0.0,45.0,0.1)
        else:
            threshold = st.sidebar.slider('Выберите γ1',0.0,45.0,0.1)
        unopt,pareto,optimal,most_optimal = Threshold(criterion,threshold).threshold_optimal(unopt,pareto)
        fig = plot_graph(unopt=unopt,pareto=pareto,optimal=optimal,most_optimal=most_optimal)

    case 'Метод идеальной точки':
        points = get_points()
        unopt,pareto = filter_optimal(points.points)
        unopt,pareto,optimal,ideal = ideal_point(points.points,unopt,pareto)
        fig = plot_graph(unopt=unopt,pareto=pareto,optimal=optimal,ideal=ideal)

st.plotly_chart(fig,use_container_width=True)