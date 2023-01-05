from pathlib import Path
import requests
from reportlab.lib.pagesizes import A4, landscape, mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from secrets import token_urlsafe
from app.models.tables import Worksheet_Content
from pptx import Presentation
from pptx.util import Mm
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from pptx.dml.color import RGBColor


ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_id_generator():
    image_id = token_urlsafe(40)
    image_id_db = Worksheet_Content.query.filter(Worksheet_Content.image_id == image_id).first()
    if image_id_db:
        image_id_generator()
    return image_id

def pdf_generator(content, image_id):
    try:
        colunas = content['colunas']
        linhas = content['conteudo']

        endereco_column = ''
        latitude_column = ''
        longitude_column = ''
        codigo_column = ''
        foto_column = None
        other_columns = []

        for coluna in colunas:
            if coluna.lower().rsplit(' ')[0] == 'endereco' or coluna.lower().rsplit(' ')[0] == 'endereço' or coluna.lower().rsplit(' ')[0] == 'direccion' or coluna.lower().rsplit(' ')[0] == 'dirección' or coluna.lower().rsplit(' ')[0] == 'address':
                endereco_column = coluna
            elif coluna.lower().rsplit(' ')[0] == 'latitude' or coluna.lower().rsplit(' ')[0] == 'latitud':
                latitude_column = coluna
            elif coluna.lower().rsplit(' ')[0] == 'longitude' or coluna.lower().rsplit(' ')[0] == 'longitud':
                longitude_column = coluna
            elif coluna.lower().rsplit(' ')[0] == 'cod.' or coluna.lower().rsplit(' ')[0] == 'codigo' or coluna.lower().rsplit(' ')[0] == 'código' or coluna.lower().rsplit(' ')[0] == 'code' or coluna.lower().rsplit(' ')[0] == 'cod' or coluna.lower().rsplit(' ')[0] == 'cód' or coluna.lower().rsplit(' ')[0] == 'cód.':
                codigo_column = coluna
            elif coluna.lower().rsplit(' ')[0] == 'foto' or coluna.lower().rsplit(' ')[0] == 'imagem' or coluna.lower().rsplit(' ')[0] == 'imagen' or coluna.lower().rsplit(' ')[0] == 'fotografia' or coluna.lower().rsplit(' ')[0] == 'fotografía' or coluna.lower().rsplit(' ')[0] == 'image' or coluna.lower().rsplit(' ')[0] == 'picture' or coluna.lower().rsplit(' ')[0] == 'photo':
                foto_column = coluna
            else:
                other_columns.append(coluna)
        if not foto_column:
            return False, 'A coluna da foto não foi reconhecida. A planilha deve fornecer uma coluna de nome "Foto", "Imagem", "Image", "Picture", "Photo", "Imagen" ou "Fotografia".'

        # Gerando PDF
        pdf = canvas.Canvas(f'app/static/media/pdf/{image_id}.pdf', landscape(A4))
        # Gerando PPTX
        apresentacao = Presentation()
        apresentacao.slide_height = Mm(210)
        apresentacao.slide_width = Mm(297)

        for i, linha in enumerate(linhas):
            image_link_separated= linha[foto_column].rsplit('/')
            image_link = image_link_separated[len(image_link_separated) - 1]
            imagem = Path(f'app/static/media/pdf_provider_images/{image_link}')
            if imagem.is_file():
                pass
            else:
                with open(f'app/static/media/pdf_provider_images/{image_link}', 'wb') as nova_imagem:
                    imagem = requests.get(linha[foto_column], stream=True)
                    if not imagem.ok:
                        print('Link de imagem inexistente.')
                        return False, 'Link de imagem inexistente.'
                    else:
                        for dado in imagem.iter_content():
                            nova_imagem.write(dado)


            coordenadas = f'{linha[latitude_column]}  {linha[longitude_column]}'

            # Inicializando PPT
            slide = apresentacao.slides.add_slide(apresentacao.slide_layouts[6])
            
            # Template de fundo PDF
            pdf.drawImage('app/static/media/pdf_provider_images/template_pdf.jpg', 0, 0, 297*mm, 210*mm)

            # Template de fundo PPTX
            template_fundo = slide.shapes.add_picture('app/static/media/pdf_provider_images/template_pdf.jpg', Mm(0), Mm(0), height=Mm(210), width=Mm(297))
            
            # Endereço PDF
            pdf.setFont('Helvetica-Bold', 20)
            pdf.setFillColor(colors.white)
            pdf.drawCentredString(142*mm,198*mm, linha[endereco_column])

            # Endereço PPTX
            endereco = slide.shapes.add_textbox(Mm(76), Mm(4), Mm(125), Mm(6))
            endereco_text_frame = endereco.text_frame
            endereco_text_frame.clear()
            endereco_text_frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
            endereco_text = endereco_text_frame.paragraphs[0].add_run()
            endereco_text.text = linha[endereco_column]
            endereco_text.font.name = 'Helvetica'
            endereco_text.font.bold = True
            endereco_text.font.size = Mm(7)
            endereco_text.font.color.rgb = RGBColor(255,255,255)

            # Imagem PDF
            pdf.drawImage(f'app/static/media/pdf_provider_images/{image_link}', 2.5*mm, 30*mm, 228.5*mm, 158.19*mm)

            #Imagem PPTX
            imagem = slide.shapes.add_picture(f'app/static/media/pdf_provider_images/{image_link}', Mm(2.5), Mm(21.81), height=Mm(158.19), width=Mm(228.5))
            
            # Coordenadas PDF
            pdf.setFont('Helvetica-Bold', 15)
            pdf.setFillColor(colors.black)
            pdf.drawString(5*mm, 21*mm, 'Coordenadas:')
            
            pdf.setFont('Helvetica', 15)
            pdf.drawString(5*mm, 11*mm, coordenadas)

            # Coordenadas PPTX
            coordenadas_pptx = slide.shapes.add_textbox(Mm(-37), Mm(182), Mm(125), Mm(6))
            coordenadas_text_frame = coordenadas_pptx.text_frame
            coordenadas_text_frame.clear()
            coordenadas_text_frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
            coordenadas_text = coordenadas_text_frame.paragraphs[0].add_run()
            coordenadas_text.text = 'Coordenadas:'
            coordenadas_text.font.name = 'Helvetica'
            coordenadas_text.font.bold = True
            coordenadas_text.font.size = Mm(6)

            coordenadas_content = slide.shapes.add_textbox(Mm(-27), Mm(192), Mm(125), Mm(6))
            coordenadas_content_text_frame = coordenadas_content.text_frame
            coordenadas_content_text_frame.clear()
            coordenadas_content_text = coordenadas_content_text_frame.paragraphs[0].add_run()
            coordenadas_content_text.text = coordenadas
            coordenadas_content_text.font.name = 'Helvetica'
            coordenadas_content_text.font.size = Mm(6)
            
            # Código PDF
            pdf.setFont('Helvetica-Bold', 15)
            pdf.drawString(130*mm, 21*mm, 'Código:')
            
            pdf.setFont('Helvetica', 15)
            pdf.drawString(130*mm, 11*mm, linha[codigo_column])

            # Código PPTX
            codigo = slide.shapes.add_textbox(Mm(80), Mm(182), Mm(125), Mm(6))
            codigo_text_frame = codigo.text_frame
            codigo_text_frame.clear()
            codigo_text_frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
            codigo_text = codigo_text_frame.paragraphs[0].add_run()
            codigo_text.text = 'Codigo:'
            codigo_text.font.name = 'Helvetica'
            codigo_text.font.bold = True
            codigo_text.font.size = Mm(6)

            codigo_content = slide.shapes.add_textbox(Mm(80), Mm(192), Mm(125), Mm(6))
            codigo_content_text_frame = codigo_content.text_frame
            codigo_content_text_frame.clear()
            codigo_content_text = codigo_content_text_frame.paragraphs[0].add_run()
            codigo_content_text.text = linha[codigo_column]
            codigo_content_text.font.name = 'Helvetica'
            codigo_content_text.font.size = Mm(6)

            eixo_y_pdf = 185
            eixo_y_pptx = 19

            for coluna in other_columns:
                # Outras Colunas PDF
                pdf.setFont('Helvetica-Bold', 12)
                pdf.drawString(235*mm, eixo_y_pdf*mm, str(coluna))
                
                pdf.setFont('Helvetica', 12)
                pdf.drawString(235*mm, (eixo_y_pdf - 5) * mm, str(linha[coluna]))
                eixo_y_pdf -= 15

                # Outras colunas PPTX
                outros = slide.shapes.add_textbox(Mm(180), Mm(eixo_y_pptx), Mm(125), Mm(6))
                outros_text_frame = outros.text_frame
                outros_text_frame.clear()
                outros_text_frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
                outros_text = outros_text_frame.paragraphs[0].add_run()
                outros_text.text = str(coluna)
                outros_text.font.name = 'Helvetica'
                outros_text.font.bold = True
                outros_text.font.size = Mm(4.48)

                outros_content = slide.shapes.add_textbox(Mm(195), Mm(eixo_y_pptx + 7), Mm(125), Mm(6))
                outros_content_text_frame = outros_content.text_frame
                outros_content_text_frame.clear()
                outros_content_text = outros_content_text_frame.paragraphs[0].add_run()
                outros_content_text.text = str(linha[coluna])
                outros_content_text.font.name = 'Helvetica'
                outros_content_text.font.size = Mm(4.48)
                eixo_y_pptx += 15
            
            # Página PDF
            pdf.setFont('Helvetica-Bold', 20)
            pdf.setFillColor(colors.white)
            pdf.drawString(285.5*mm, 7*mm, str(pdf.getPageNumber()))

            # Página PPTX
            pagina = slide.shapes.add_textbox(Mm(225), Mm(194), Mm(125), Mm(6))
            pagina_text_frame = pagina.text_frame
            pagina_text_frame.clear()
            pagina_text_frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
            pagina_text = pagina_text_frame.paragraphs[0].add_run()
            pagina_text.text = str(pdf.getPageNumber())
            pagina_text.font.name = 'Helvetica'
            pagina_text.font.bold = True
            pagina_text.font.size = Mm(8)
            pagina_text.font.color.rgb = RGBColor(255,255,255)
            
            pdf.showPage()
        pdf.save()
        apresentacao.save(f'app/static/media/pptx/{image_id}.pptx')
        return True, 'Arquivos PDF e PPTX gerados com sucesso.'
    except Exception as error:
        print(str(error))
        return False, 'Erro no servidor. Tente novamente.'