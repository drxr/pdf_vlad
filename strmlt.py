import streamlit as st
from datetime import datetime
from pdf_functions import create_pdf, add_text_to_existing_pdf


nowaday = datetime.today().date()
now_month = datetime.today().month
now_year = datetime.today().year
current_date = datetime(now_year, now_month, 1).date()

st.title('**Генератор PDF для Влада**')
st.text('Добавьте все данные для генерации благодарственного письма')

project_name = st.text_input('Введите название проекта:', value=None)

if project_name is not None:
    st.write('**Проект:** ',project_name)

description = st.text_input('Введите описание проекта (данный проект предполагал): ')

if description is not None:
    st.write('Описание добавлено')

start_date = st.date_input('Введите дату начала проекта:', value=None, format='DD.MM.YYYY')

if start_date is not None:
    start_date = start_date.strftime('%d.%m.%Y')

finish_date = st.date_input('Введите дату окончания проекта:', value=None, format='DD.MM.YYYY')

if finish_date is not None:
    finish_date = finish_date.strftime('%d.%m.%Y')

if start_date is not None and finish_date is not None:
    st.write(f'Период проекта с {start_date} по {finish_date}')



student = st.text_input('Введите имя и фамилию студента через пробел:', value=None)

if student is not None:
    name, last_name = student.split(' ')

role = st.text_input('Введите роль студента на проекте (в родительном падеже): ')

if role is not None:
    st.write('**Роль студента:**', role)

tasks_raw = st.text_area('Введите задачи студента в рамках проекта: ')

if tasks_raw is not None:
    tasks = tasks_raw.split('\n')

if project_name is not None and description is not None and tasks_raw is not None and student is not None and role is not None:
    if st.button('Начать генерацию'):
        create_pdf('example.pdf', name, last_name, project_name, start_date, finish_date, role, description, tasks)
        add_text_to_existing_pdf()

        st.download_button(
            help='Файл с благодарственным письмом для студента',
            label="Скачать pdf :sunglasses:",
            data=open('student.pdf', 'rb').read(),
            file_name='student.pdf',
            mime='application/pdf'
            )
