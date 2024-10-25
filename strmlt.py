import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime
import zipfile
import os


def create_pdf(filename: str, 
               user_name: str, 
               user_lastname: str, 
               project_name: str, 
               start_date: str, 
               end_date: str, 
               role: str, 
               description: str, 
               some_tasks: list[str],
               marker: str) -> None:
    
    '''
    Функция для генерации текст для файла с шаблоном дизайна.

    Аргументы:

    - filename -> название временного файла в формате название_файла.pdf
    - user_name, user_lastname -> имя и фамилия человека
    - project_name -> название проекта
    - start_date, end_date -> даты начала и окончания проекта
    - role -> роль студента в проекте (техлид, участник, проектный менеджер и так далее)
    - description -> описание проекта
    - some_tasks -> список задач, реализованных студентом в рамках проекта
    - marker -> пол студента (задается в поле ввода имени и фамилии студента)
    '''

    # Регистрируем шрифт яндекс регуляр (файл ttf со шрифтом должен быть в папке проекта)
    pdfmetrics.registerFont(TTFont('YS Text-Regular', 'yst.ttf'))

    # Создаем объект документа с заданными размерами
    doc = SimpleDocTemplate(filename, 
                            pagesize=A4,  # размер документа
                            leftMargin=0.6 * inch,  # Левое поле
                            rightMargin=2.7 * inch,  # Правое поле
                            topMargin=3 * inch,  # Верхнее поле
                            bottomMargin=0.5 * inch  # Нижнее поле
        )

    # Создаем стили для элементов документа
    styles = getSampleStyleSheet()

    # стиль для текстовых элементов документа
    style = ParagraphStyle(
        name='Normal',
        fontName='YS Text-Regular',
        fontSize=12,
        leading=14,
        spaceBefore=1.3,
        spaceAfter=1.3,
        textColor='white',
        firstLineIndent=24,
        alignment=4,
    )

    # стиль для задач (аргумент some_tasks)
    style_2 = ParagraphStyle(
        name='Normal',
        fontName='YS Text-Regular',
        fontSize=12,
        leading=14,
        spaceBefore=1.3,
        spaceAfter=1.3,
        textColor='white',
    )

    # стиль для даты
    date_style = ParagraphStyle(
        name='Date',
        fontName='YS Text-Regular',
        fontSize=12,
        leading=12,
        alignment=2, 
        textColor='white'
    )

    # Создаем список элементов для документа
    elements = []

    # Текст для документа
    text_1m = f'''
    <font color='crimson'><b>{user_name} {user_lastname}</b></font> принимал участие в проекте 
    <font color='crimson'><b>«{project_name}»</b></font> в период с {start_date} по {end_date} 
    в качестве <font color='crimson'><b>{role}</b></font>. Данный проект предполагал {description}.
    Во время проекта <font color='crimson'>{user_name}</font> справился успешно со следующими 
    задачами:'''

    text_2m = f'''
    На данный момент проект успешно завершен, продукт используется клиентом. Предполагается его 
    дальнейшее развитие.
    '''

    text_3m = f'''
    Во время работы над проектом <font color='crimson'>{user_name}</font> продемонстрировал 
    способность быстро погружаться в задачи по проекту, отличное понимание технических требований, 
    а также внимательность к деталям и прекрасные коммуникативные навыки внутри команды.
    '''

    text_4m = f'''
    Мы уверены, что <font color='crimson'>{user_name}</font> обладает необходимыми знаниями и 
    навыками для успешной работы в области управления IT-проектами, и рекомендуем его для 
    дальнейшего трудоустройства.
    '''

    text_1f = f'''
    <font color='crimson'><b>{user_name} {user_lastname}</b></font> принимала участие в проекте 
    <font color='crimson'><b>«{project_name}»</b></font> в период с {start_date} по {end_date} 
    в качестве <font color='crimson'><b>{role}</b></font>. Данный проект предполагал {description}.
    Во время проекта <font color='crimson'>{user_name}</font> успешно справилась со следующими 
    задачами:'''

    text_2f = f'''
    На данный момент проект успешно завершен, продукт используется клиентом. Предполагается его 
    дальнейшее развитие.
    '''

    text_3f = f'''
    Во время работы над проектом <font color='crimson'>{user_name}</font> продемонстрировала 
    способность быстро погружаться в задачи по проекту, отличное понимание технических требований, 
    а также внимательность к деталям и прекрасные коммуникативные навыки внутри команды.
    '''

    text_4f = f'''
    Мы уверены, что <font color='crimson'>{user_name}</font> обладает необходимыми знаниями и 
    навыками для успешной работы в области управления IT-проектами, и рекомендуем ее для 
    дальнейшего трудоустройства.
    '''
    if marker == 'м':
        # Добавляем текст с автопереносом
        elements.append(Paragraph(text_1m, style))
        # Добавляем пробел между абзацами
        elements.append(Spacer(1, 3))

        # добавляем задачи
        for el in some_tasks:
            elements.append(Paragraph(el, style_2))
        elements.append(Spacer(1, 3))
        
        elements.append(Paragraph(text_2m, style))
        elements.append(Spacer(1, 3))

        elements.append(Paragraph(text_3m, style))
        elements.append(Spacer(1, 3))

        elements.append(Paragraph(text_4m, style))
        elements.append(Spacer(1, 20))

        # добавляем текущую дату в документ
        current_date = datetime.now().strftime('%d.%m.%Y')
        date_paragraph = Paragraph(current_date, date_style)
        elements.append(date_paragraph)

        # Создаем PDF-документ
        doc.build(elements)

    elif marker == 'ж':
        # Добавляем текст с автопереносом
        elements.append(Paragraph(text_1f, style))
        # Добавляем пробел между абзацами
        elements.append(Spacer(1, 3))

        # добавляем задачи
        for el in some_tasks:
            elements.append(Paragraph(el, style_2))
        elements.append(Spacer(1, 3))
        
        elements.append(Paragraph(text_2f, style))
        elements.append(Spacer(1, 3))

        elements.append(Paragraph(text_3f, style))
        elements.append(Spacer(1, 3))

        elements.append(Paragraph(text_4f, style))
        elements.append(Spacer(1, 20))

        # добавляем текущую дату в документ
        current_date = datetime.now().strftime('%d.%m.%Y')
        date_paragraph = Paragraph(current_date, date_style)
        elements.append(date_paragraph)

        # Создаем PDF-документ
        doc.build(elements)


def add_text_to_existing_pdf(filename) -> None:

    '''Добавляет текст, созданный функцией create_pdf к файлу шаблона 
    sample2.pdf и создает новый файл с благодарственным письмом
    '''

    # читаем созданный функцией create_pdf файл
    new_pdf = PdfReader(filename)
        
    # читаем файл с шаблоном
    existing_pdf = PdfReader('sample2.pdf', "rb")
    output = PdfWriter()
    
    # соединяем оба файла
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    
    # сохраняем итоговый файл
    output_stream = open(filename, "wb")
    output.write(output_stream)
    output_stream.close()


nowaday = datetime.today().date()
now_month = datetime.today().month
now_year = datetime.today().year
current_date = datetime(now_year, now_month, 1).date()


st.title('**Генератор PDF для рекомендательных писем**')
st.text('Кнопка генерации писем появится после внесения данных во все поля')

project_name = st.text_input('**Введите название проекта:**', value=None)

if project_name is not None:
    st.write('**Проект:** ', project_name)

description = st.text_input('**Введите описание проекта** (данный проект предполагал): ', value=None)

if description is not None:
    st.write('**Описание:** ', description)

start_date = st.date_input('**Введите дату начала проекта:**', value=None, format='DD.MM.YYYY')

if start_date is not None:
    start_date = start_date.strftime('%d.%m.%Y')

finish_date = st.date_input('**Введите дату окончания проекта:**', value=None, format='DD.MM.YYYY')

if finish_date is not None:
    finish_date = finish_date.strftime('%d.%m.%Y')

if start_date is not None and finish_date is not None:
    st.write(f'**Период проекта:** с {start_date} по {finish_date}')

role = st.text_input('**Введите роль студента на проекте** (в родительном падеже): ', value=None)

if role is not None:
    st.write('**Роль студента:** ', role)

tasks_raw = st.text_area('**Введите задачи студента в рамках проекта:** ')

if tasks_raw is not None:
    tasks = tasks_raw.split('\n')

st.write('---')
st.text('Ввведите имя, фамилию и пол студента через пробел')
st.markdown('Пример: **Маша Петрова ж** или **Иван Серов м**')
st.text('Если студентов несколько, то каждый следующий студент вносится с новой строки')
st.write('---')

students_raw = st.text_area('Введите имя, фамилию и пол студента:', value=None)

if students_raw is not None:
    students_list = students_raw.split('\n')
    for num, student in enumerate(students_list):
        if student.split(' ')[-1].lower() not in ['м', 'ж']:
            st.write(num, 'Студент внесен не корректно')
        else:
            st.write(num, 'Студент внесен корректно')  


if project_name is not None and description is not None and tasks_raw is not None and students_raw is not None and role is not None:
    if st.button('Начать генерацию'):

        students_letters = []

        for student in students_list:
            name, last_name, marker = (
            student.split(' ')[0],
            student.split(' ')[1], 
            student.split(' ')[-1]
            )

            name_of_file = name + '_' + last_name + '.pdf'
            create_pdf(name_of_file, name, last_name, project_name, start_date, finish_date, role, description, tasks, marker)
            add_text_to_existing_pdf(name_of_file)
            students_letters.append(name_of_file)
        
        with zipfile.ZipFile('students.zip', 'w') as my_zip:
            for letter in students_letters:
                my_zip.write(letter)
        
        for file in os.listdir():
            if file.endswith('pdf') and 'sample' not in file:
                os.remove(file)

        st.download_button(
            help='Архив с благодарственными письмами для студентов',
            label="Скачать архив :sunglasses:",
            data=open('students.zip', 'rb').read(),
            file_name='student.zip',
            mime='application/zip'
            )
