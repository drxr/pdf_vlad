from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime


def create_pdf(filename: str, 
               user_name: str, 
               user_lastname: str, 
               project_name: str, 
               start_date: str, 
               end_date: str, 
               role: str, 
               description: str, 
               some_tasks: list[str]) -> None:
    
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
    text_1 = f'''
    <font color='crimson'><b>{user_name} {user_lastname}</b></font> принимал(а) участие в проекте 
    <font color='crimson'><b>«{project_name}»</b></font>     в период с {start_date} по {end_date} 
    в качестве <font color='crimson'><b>{role}</b></font>.     Данный проект предполагал {description}.
    Во время проекта <font color='crimson'>{user_name}</font> справился(-ась) успешно со следующими 
    задачами:'''

    text_2 = f'''
    На данный момент проект успешно завершен, продукт используется клиентом. Предполагается его 
    дальнейшее развитие.
    '''

    text_3=f'''
    Во время работы над проектом <font color='crimson'>{user_name}</font> продемонстрировал(а) 
    способность быстро погружаться в задачи по проекту, отличное понимание технических требований, 
    а также внимательность к деталям и прекрасные коммуникативные навыки внутри команды.
    '''

    text_4=f'''
    Мы уверены, что <font color='crimson'>{user_name}</font> обладает необходимыми знаниями и 
    навыками для успешной работы в области управления IT-проектами, и рекомендуем его/ее для 
    дальнейшего трудоустройства.
    '''

    # Добавляем текст с автопереносом
    elements.append(Paragraph(text_1, style))
    # Добавляем пробел между абзацами
    elements.append(Spacer(1, 3))

    # добавляем задачи
    for el in some_tasks:
        elements.append(Paragraph(el, style_2))
    elements.append(Spacer(1, 3))
    
    elements.append(Paragraph(text_2, style))
    elements.append(Spacer(1, 3))

    elements.append(Paragraph(text_3, style))
    elements.append(Spacer(1, 3))

    elements.append(Paragraph(text_4, style))
    elements.append(Spacer(1, 20))

    # добавляем текущую дату в документ
    current_date = datetime.now().strftime('%d.%m.%Y')
    date_paragraph = Paragraph(current_date, date_style)
    elements.append(date_paragraph)

    # Создаем PDF-документ
    doc.build(elements)


def add_text_to_existing_pdf() -> None:

    '''Добавляет текст, созданный функцией create_pdf к файлу шаблона 
    sample2.pdf и создает новый файл с благодарственным письмом
    '''

    # читаем созданный функцией create_pdf файл
    new_pdf = PdfReader('example.pdf')
        
    # читаем файл с шаблоном
    existing_pdf = PdfReader('sample2.pdf', "rb")
    output = PdfWriter()
    
    # соединяем оба файла
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    
    # сохраняем итоговый файл
    output_stream = open('student' + ".pdf", "wb")
    output.write(output_stream)
    output_stream.close()
