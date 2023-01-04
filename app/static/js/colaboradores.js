import { Colaborador } from "./classes.js"

var colaboradores = []
var menu = document.querySelector('#menu')
var lista = document.querySelector('#lista')

var alertGenerate = function(parentElement, text) {
    let alert = document.createElement('div')
    alert.className = 'alert alert-warning alert-dismissible fade show'
        alert.role = 'alert'
        alert.innerHTML = `
            ${text}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `
    parentElement.insertAdjacentElement('afterbegin', alert)
}

var atualizarLista = function() {
    lista.innerHTML = ''
    colaboradores.forEach(element => {
        let colaboradorNome = element.name != null ? (element.name).replace(/(^\w{1})|(\s+\w{1})/g, letra => letra.toUpperCase()) : null
        let colaboradorId = element.id
        let colaboradorEmail = element.email
        
        let linha = document.createElement('div')
        linha.className = 'linha'
        
        let nome = document.createElement('div')
        nome.className = 'linha-nome'
        nome.innerHTML = colaboradorNome
        
        //Botão visualizar
        let visualizar = document.createElement('div')
        visualizar.className = 'linha-bt'

        let visualizarBt = document.createElement('button')
        visualizarBt.type = 'button'
        visualizarBt.className = 'btn btn-sm btn-warning linha-bt-bt'
        visualizarBt.setAttribute('data-bs-toggle', 'modal')
        visualizarBt.innerHTML = 'Visualizar'
        visualizarBt.addEventListener('click', () => {
            $(`#visualizar${element.id}`).modal('show')
        })
        visualizar.appendChild(visualizarBt)

        let visualizarModal = document.createElement('div')
        visualizarModal.className = 'modal fade'
        visualizarModal.id = `visualizar${element.id}`
        visualizarModal.tabIndex = '-1'
        visualizar.ariaLabel = `exampleModalLabelVisualizar${element.id}`
        visualizarModal.ariaHidden = true
        visualizarModal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabelVisualizar${element.id}">${colaboradorNome}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div class="visualizar-item">
                        <p class="label-item">Nome:</p>
                        <p class="conteudo-item">${colaboradorNome}</p>
                    </div>
                    <div class="visualizar-item">
                        <p class="label-item">E-mail:</p>
                        <p class="conteudo-item">${colaboradorEmail}</p>
                    </div>
                    <div class="visualizar-item">
                        <p class="label-item">Acesso:</p>
                        <p class="conteudo-item">Colaborador</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                </div>
            </div>
        </div>
        `
        visualizar.appendChild(visualizarModal)

        //Botão editar
        let editar = document.createElement('div')
        editar.className = 'linha-bt'

        let editarBt = document.createElement('button')
        editarBt.type = 'button'
        editarBt.className = 'btn btn-sm btn-primary linha-bt-bt'
        editarBt.setAttribute('data-bs-toggle', 'modal')
        editarBt.innerHTML = 'Editar'
        editarBt.addEventListener('click', () => {
            $(`#editar${element.id}`).modal('show')
        })
        editar.appendChild(editarBt)

        let editarModal = document.createElement('div')
        editarModal.className = 'modal fade'
        editarModal.id = `editar${element.id}`
        editarModal.tabIndex = '-1'
        editarModal.ariaLabel = `exampleModalLabelEditar${element.id}`
        editarModal.ariaHidden = true
        editarModal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabelEditar${element.id}">${colaboradorNome}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form id="editarForm${element.id}" action="/pdfservice/painel-administrativo/colaboradores" method="post">
                        <input type="hidden" name="tipo" value="editar">
                        <input type="hidden" name="id" value="${element.id}">
                        <div class="visualizar-item">
                            <p class="label-item">Nome:</p>
                            <input required maxlength="50" type="text" class="input-edit" name="nome-edit" id="nome-edit${element.id}" value="${colaboradorNome}">
                        </div>
                        <div class="visualizar-item">
                            <p class="label-item">E-mail:</p>
                            <input required maxlength="50" type="text" class="input-edit" name="email-edit" id="email-edit${element.id}" value="${colaboradorEmail}">
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button id="formBt${element.id}" type="submit" class="btn btn-warning">Confirmar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        `
        editar.appendChild(editarModal)

        //Botão nova senha
        let novaSenha = document.createElement('div')
        novaSenha.className = 'linha-bt'

        let novaSenhaBt = document.createElement('button')
        novaSenhaBt.type = 'button'
        novaSenhaBt.className = 'btn btn-sm btn-info linha-bt-bt'
        novaSenhaBt.setAttribute('data-bs-toggle', 'modal')
        novaSenhaBt.innerHTML = 'Nova Senha'
        novaSenhaBt.addEventListener('click', () => {
            $(`#novaSenha${element.id}`).modal('show')
        })
        novaSenha.appendChild(novaSenhaBt)

        let novaSenhaModal = document.createElement('div')
        novaSenhaModal.className = 'modal'
        novaSenhaModal.classList.add('fade')
        novaSenhaModal.id = `novaSenha${element.id}`
        novaSenhaModal.tabIndex = '-1'
        novaSenhaModal.setAttribute('aria-labelledby', `exampleModalLabelNovaSenha${element.id}`)
        novaSenhaModal.ariaHidden = true
        novaSenhaModal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabeleditar">Nova Senha - ${colaboradorNome}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form action="/pdfservice/painel-administrativo/colaboradores" method="POST">
                    <input type="hidden" name="tipo" value="nova-senha">
                    <input type="hidden" name="id" value="${element.id}">
                    <div class="modal-body">
                        <div class="visualizar-item">
                            <p class="label-item">Nova Senha:</p>
                            <input required maxlength="50" type="password" class="input-edit" name="senha">
                        </div>
                        <div class="visualizar-item">
                            <p class="label-item">Confirmar Senha:</p>
                            <input required maxlength="50" type="password" class="input-edit" name="senha2">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="btn btn-warning">Confirmar</button>
                    </div>
                </form>
            </div>
        </div>
        `
        novaSenha.appendChild(novaSenhaModal)

        //Botão excluir
        let excluir = document.createElement('div')
        excluir.className = 'linha-bt'

        let excluirBt = document.createElement('button')
        excluirBt.type = 'button'
        excluirBt.className = 'btn btn-sm btn-secondary linha-bt-bt'
        excluirBt.setAttribute('data-bs-toggle', 'modal')
        excluirBt.innerHTML = 'Remover'
        excluirBt.addEventListener('click', () => {
            $(`#excluir${element.id}`).modal('show')
        })
        excluir.appendChild(excluirBt)

        let excluirModal = document.createElement('div')
        excluirModal.className = 'modal'
        excluirModal.classList.add('fade')
        excluirModal.id = `excluir${element.id}`
        excluirModal.tabIndex = '-1'
        excluirModal.setAttribute('aria-labelledby', `exampleModalLabelExcluir${element.id}`)
        excluirModal.ariaHidden = true
        excluirModal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabelexcluir">Tem certeza?</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                Após a exclusão, todo o cadastro de ${colaboradorNome} será apagado.
                </div>
                <form action="/pdfservice/painel-administrativo/colaboradores" method="POST">
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <input type="hidden" name="tipo" value="excluir">
                        <input type="hidden" name="id" value="${element.id}">
                        <button type="submit" class="btn btn-warning">Confirmar</button>
                    </div>
                </form>
            </div>
        </div>
        `
        excluir.appendChild(excluirModal)
        
        linha.appendChild(nome)
        linha.appendChild(visualizar)
        linha.appendChild(editar)
        linha.appendChild(novaSenha)
        linha.appendChild(excluir)
        lista.appendChild(linha)
    });
}
var carregarLista = function() {
    lista.innerHTML = `
    <div class="spinner-border text-warning" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
    `
    fetch('/pdfservice/painel-administrativo/colaboradores?filter=all')
    .then(function(response) {
        if (response.ok) {
            return response.json()
            .then(function(data) {
                data.forEach(element => {
                    let colaborador = new Colaborador(
                        element.id,
                        element.name,
                        element.email,
                        null
                    )
                    colaboradores.push(colaborador)
                });
                atualizarLista()
            })
        } else {
            lista.innerHTML = ''
            alertGenerate(menu, 'Erro ao carregar os Dados. Tente novamente.')
        }
    })
    
}

window.onload = function() {
    carregarLista()
} 