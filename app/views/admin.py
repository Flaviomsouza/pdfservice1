from flask import Blueprint, flash, make_response, render_template, redirect, request, Response, get_flashed_messages
from app.models.basemodels import  User_For_View_, Worksheet_For_View_
from pymysql.err import IntegrityError as IntegrityError2
from app.providers.hash_provider import check_password, hash_generate
from app.models.tables import User, Worksheet_Content
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta
from flask_login import current_user, login_required, login_user, logout_user
from json import dumps, loads
import pandas as pd
from app import db
from app.providers.functions import allowed_file, image_id_generator, pdf_generator
import os
from rq import Queue
from worker import conn
import redis

redis_db = redis.Redis(decode_responses=True, host=os.environ['REDIS_HOST'], username=os.environ['REDIS_USERNAME'], password=os.environ['REDIS_PASSWORD'], port=15022)

admin_bp = Blueprint(
    'admin_bp',
    __name__,
    url_prefix='/pdfservice'
)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if current_user.name:
            return redirect('/pdfservice/painel-administrativo')
    except:
        pass
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = User.query.filter(User.email == email).first()
        if not user:
            flash('Usuário Inválido')
            return redirect('/pdfservice/login')
        elif not check_password(senha, user.hash):
            flash('Senha Inválida')
            return redirect('/pdfservice/login')
        else:
            login_user(user, remember=True)

        return redirect('/pdfservice/painel-administrativo')
    else:
        return render_template('login.html')

@admin_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/pdfservice/login')

@admin_bp.route('/painel-administrativo', methods=['GET'])
@login_required
def painel_administrativo():
    return render_template('painel-administrativo.html')

@admin_bp.route('/painel-administrativo/colaboradores', methods=['GET', 'POST'])
@login_required
def colaboradores():
    try:
        if current_user.is_admin:
            pass
        else:
            flash('Você não tem permissão para acessar esta página.')
            return redirect('/pdfservice/painel-administrativo')
        if request.method == 'POST':
            tipo = request.form.get('tipo')
            if tipo == 'editar':
                id = request.form.get('id')
                nome = request.form.get('nome-edit')
                email = request.form.get('email-edit')
                
                user_db = User.query.filter(User.id == id).first()
                user_db.name = nome if nome else user_db.name
                user_db.email = email if email else user_db.email
                db.session.add(user_db)
                db.session.commit()
                flash('Alteração efetuada com sucesso.')
            elif tipo == 'excluir':
                id = request.form.get('id')
                user_to_del = User.query.filter(User.id == id).first()
                db.session.delete(user_to_del)
                db.session.commit()
                flash('Colaborador removido com sucesso.')
            elif tipo == 'nova-senha':
                senha = request.form.get('senha')
                senha2 = request.form.get('senha2')
                id = request.form.get('id')
                if len(senha) < 8:
                    flash('Sua senha deve conter ao menos 8 dígitos.')
                elif senha != senha2:
                    flash('As senhas não conferem.')
                else:
                    hash = hash_generate(senha)
                    user_db = User.query.filter(User.id == id).first()
                    user_db.hash = hash if hash else user_db.hash
                    db.session.add(user_db)
                    db.session.commit()
                    flash('Alteração de senha efetuada com sucesso.')
            elif tipo == 'adicionar':
                nome = request.form.get('nome')
                email = request.form.get('email')
                senha = request.form.get('senha')
                senha2 = request.form.get('senha2')

                if senha != senha2:
                    flash('As senhas não conferem.')
                else:
                    hash = hash_generate(senha)
                    db.session.add(User(nome, email, hash, False, True))
                    db.session.commit()
                    flash('Colaborador adicionado com sucesso.')
            else:
                flash('Erro na requisição. Tente novamente')
            return redirect('/pdfservice/painel-administrativo/colaboradores')
        else:
            if request.args.get('filter'):
                filtro = request.args.get('filter')
                if filtro == 'all':
                    lista_db = User.query.filter(User.is_collaborator == True).all()
                    for i, item in enumerate(lista_db):
                        user = User_For_View_(
                            id=item.id,
                            name=item.name,
                            email=item.email,
                            is_admin=item.is_admin,
                            is_collaborator=item.is_collaborator
                        )
                        lista_db[i] = user.dict()

                    return dumps(lista_db)
            return render_template('colaboradores.html')
    
    except IntegrityError as error:
        if 'Duplicate entry' in str(error) and "for key 'users.email" in str(error):
            flash('Já existe cadastro para esse e-mail.')
        else:
            flash('Erro no servidor. Tente novamente.')
        return redirect('/pdfservice/painel-administrativo/colaboradores')
    except IntegrityError2 as error:
        if 'Duplicate entry' in str(error) and "for key 'users.email" in str(error):
            flash('Já existe cadastro para esse e-mail.')
        else:
            flash('Erro no servidor. Tente novamente.')
        return redirect('/pdfservice/painel-administrativo/colaboradores')
    except:
        flash('Erro no servidor. Tente novamente.')
        return redirect('/pdfservice/painel-administrativo')

@admin_bp.route('/painel-administrativo/novo-book', methods=['GET', 'POST'])
@login_required
def novo_book():
    if request.method == 'POST':
        try:
            nome = request.form.get('nome')
            cliente = request.form.get('cliente') if request.form.get('cliente') else None
            pessoa = request.form.get('pessoa') if request.form.get('pessoa') else None
            if not nome:
                flash('Você deve fornecer um nome para o novo book.')
                return redirect('/pdfservice/painel-administrativo/novo-book')
            arquivo = request.files.get('input-file')
            if not arquivo or arquivo.filename == '':
                flash('Nenhum arquivo foi enviado.')
            elif not allowed_file(arquivo.filename):
                flash('Formato de arquivo não suportado. Você deve enviar arquivos ".xlsx" ou ".xls"')
            else:
                tabela = pd.ExcelFile(arquivo)
                planilhas = tabela.sheet_names # Pega o nome de todas as abas da tabela
                planilhas_não_convertidas = []
                for planilha in planilhas:
                    colunas = list(pd.read_excel(arquivo, sheet_name=planilha).columns)
                    # Verifica se as colunas Endereço e Foto estão presentes
                    endereco_check = False
                    foto_check = False
                    latitude_check = False
                    longitude_check = False
                    codigo_check = False
                    for i, coluna in enumerate(colunas):
                        if 'endereço' in coluna.lower() or 'endereco' in coluna.lower() or 'direccion' in coluna.lower() or 'dirección' in coluna.lower() or 'address' in coluna.lower():
                            endereco_check = True
                        elif 'foto' in coluna.lower() or 'imagem' in coluna.lower() or 'imagen' in coluna.lower() or 'fotografia' in coluna.lower() or 'fotografía' in coluna.lower() or 'image' in coluna.lower() or 'picture' in coluna.lower() or 'photo' in coluna.lower():
                            foto_check = True
                        elif 'latitude' in coluna.lower() or 'latitud' in coluna.lower():
                            latitude_check = True
                        elif 'longitude' in coluna.lower() or 'longitud' in coluna.lower():
                            longitude_check = True
                        elif 'codigo' in coluna.lower() or 'código' in coluna.lower() or 'cod' in coluna.lower() or 'cód' in coluna.lower() or 'code' in coluna.lower():
                            codigo_check = True
                        colunas[i] = coluna
                    if not foto_check or not endereco_check or not latitude_check or not longitude_check or not codigo_check:
                        planilhas_não_convertidas.append(planilha)
                        continue
                    
                    book = pd.read_excel(arquivo, sheet_name=planilha).to_dict('records')
                    image_id = image_id_generator()
                    capa = {'nome': nome, 'cliente': cliente, 'pessoa': pessoa}
                    content = {'colunas': colunas, 'conteudo': book}
                    
                    # Criando fila rq
                    q = Queue(connection=conn)
                    # Gerando PDF
                    # pdf = pdf_generator(capa, content, image_id)
                    result = q.enqueue(pdf_generator, capa, content, image_id, True, job_timeout='30m')
                    flash(f'O book {nome.title()} está sendo gerado. Quando estiver concluído, ele aparecerá em "Lista de Books" ou notificará na tela em caso de erro.')

                if len(planilhas_não_convertidas) > 0:
                    flash_text = 'As seguintes planilhas não puderam ser convertidas: '
                    for item in planilhas_não_convertidas:
                        texto = flash_text + f'{item}, '
                        flash_text = texto
                    flash_text = f'''
                    {flash_text} .
                    Motivo: Alguma coluna obrigatória não foi reconhecida.
                    As colunas obrigatórias são código, endereço, foto, latitude e longitude.
                    Esses termos em espanhol e em inglês também são aceitos.
                    '''
                    flash(flash_text)
                    
            return redirect('/pdfservice/painel-administrativo/novo-book')
        except Exception as error:
            flash('Erro no servidor. Tente novamente.')
            return redirect('/pdfservice/painel-administrativo/novo-book')

    else:
        return render_template('novo-book.html')

@admin_bp.route('/painel-administrativo/lista-de-books', methods=['GET', 'POST'])
@login_required
def lista_de_books():
    try:
        if request.method == 'POST':
            if request.form.get('tipo') == 'excluir':
                id = request.form.get('id')
                book = Worksheet_Content.query.filter(Worksheet_Content.id == id).first()
                book_pdf = f'app/static/media/pdf/{book.image_id}.pdf'
                book_pptx = f'app/static/media/pptx/{book.image_id}.pptx'
                if os.path.exists(book_pdf):
                    os.remove(book_pdf)
                if os.path.exists(book_pptx):
                    os.remove(book_pptx)
                db.session.delete(book)
                db.session.commit()
                flash('Book removido com sucesso.')
            elif request.form.get('tipo') == 'remover-antigos':
                data_limite = date.today() - timedelta(days=60)
                books = Worksheet_Content.query.filter(Worksheet_Content.creation_date < data_limite).all()
                for book in books:
                    book_pdf = f'app/static/media/pdf/{book.image_id}.pdf'
                    book_pptx = f'app/static/media/pptx/{book.image_id}.pptx'
                    if os.path.exists(book_pdf):
                        os.remove(book_pdf)
                    if os.path.exists(book_pptx):
                        os.remove(book_pptx)
                    db.session.delete(book)
                db.session.commit()
                flash('Cadastros antigos removidos com sucesso.')
            return redirect('/pdfservice/painel-administrativo/lista-de-books')
        else:
            messages = redis_db.get('messages')
            if messages:
                message_list = messages.split('&')
                for message in message_list:
                    if len(message) > 2:
                        flash(message)
                redis_db.delete('messages')
            filtro = request.args.get('filter')
            if filtro:
                if filtro == 'all':
                    books_db = Worksheet_Content.query.all()
                    for i, item in enumerate(books_db):
                        book = Worksheet_For_View_(
                            id=item.id,
                            title=item.title,
                            creation_date=item.creation_date,
                            image_id=item.image_id
                        )
                        books_db[i] = book.dict()
                    books = sorted(books_db, key=lambda row:row['creation_date'], reverse=True)
                    return dumps(books, default=str)
                elif filtro == 'downloadpdf':
                    arquivo = request.args.get('arg')
                    try:
                        with open(f'app/static/media/pdf/{arquivo}', 'rb') as f: 
                            dados = f.read()
                        return make_response(dados, {'content-type': 'application/pdf'})
                    except FileNotFoundError:
                        flash('Arquivo não encontrado, possivelmente excluído em manutenção de rotina do servidor. Você deve gerá-lo novamente.')
                        return redirect('/pdfservice/painel-administrativo/lista-de-books')
                    except:
                        flash('Erro no servidor. Estamos trabalhando para corrigir.')
                        return redirect('/pdfservice/painel-administrativo/lista-de-books')
                elif filtro == 'downloadpptx':
                    try:
                        arquivo = request.args.get('arg')
                        with open(f'app/static/media/pptx/{arquivo}', 'rb') as f: 
                            dados = f.read()
                        return make_response(dados, {'content-type': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'})
                    except FileNotFoundError:
                        flash('Arquivo não encontrado, possivelmente excluído em manutenção de rotina do servidor. Você deve gerá-lo novamente.')
                        return redirect('/pdfservice/painel-administrativo/lista-de-books')
                    except:
                        flash('Erro no servidor. Estamos trabalhando para corrigir.')
                        return redirect('/pdfservice/painel-administrativo/lista-de-books')
                elif filtro == 'gerarNovamente':
                    id = int(request.args.get('arg'))
                    book = Worksheet_Content.query.filter(Worksheet_Content.id == id).first()
                    print(f'Book = {book}')
                    capa = {'nome':book.title, 'cliente':book.company, 'pessoa':book.person}
                    content = loads(book.content)
                    image_id = book.image_id
                    pdf = pdf_generator(capa, content, image_id)
                    if pdf[0] == False:
                        flash(pdf[1])
                        return redirect('/pdfservice/painel-administrativo/lista-de-books')
                    else:
                        flash(pdf[1])
            
            return render_template('lista-de-books.html')
    except Exception as error:
        print(str(error))
        flash('Erro no servidor. Tente novamente.')
        return redirect('/pdfservice/painel-administrativo')

@admin_bp.route('/pdfview/<pdf_file>')
def pdfview(pdf_file):
    try:
        with open(f'app/static/media/pdf/{pdf_file}', 'rb') as f: 
            dados = f.read()
        return make_response(dados, {'content-type': 'application/pdf'})
    except FileNotFoundError:
        return 'Link inexistente. Contate o servidor. (Erro: Arquivo não encontrado)'
    except:
        return 'Erro no servidor. Estamos trabalhando para corrigir.'

@admin_bp.route('/flash-message-generate')
def flash_message_generate():
    chave = request.headers.get('Secret-Key')
    message = request.args.get('message')
    if chave == os.environ['SECRET_KEY']:
        redis_db.append('messages', f'{message}&')
        return Response(status=200, response='OK')
    return dumps(False)
