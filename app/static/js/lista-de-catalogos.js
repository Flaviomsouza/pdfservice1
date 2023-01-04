import { Catalogo } from "./classes.js";

var catalogos = []
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

function carregarLista() {
    lista.innerHTML = `
    <div class="spinner-border text-warning" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
    `
    let listaCatalogos = fetch('/pdfservice/painel-administrativo/lista-de-catalogos?filter=all')
    .then(function(response) {
        if (response.ok) {
            return response.json()
            .then(function(data) {
                data.forEach(element => {
                    let ano = element.creation_date.substring(0, 4)
                    let mes = element.creation_date.substring(5, 7)
                    let dia = element.creation_date.substring(8, 10)
                    let catalogo = new Catalogo(
                        element.id,
                        element.title,
                        element.content,
                        `${dia}/${mes}/${ano}`,
                        element.image_id,
                    )
                    catalogos.push(catalogo)
                });
                atualizarLista()
            })
        } else {
            lista.innerHTML = ''
            alertGenerate(menu, 'Erro ao carregar os Dados. Tente novamente.')
        }
    })
}

function atualizarLista() {
    lista.innerHTML = ''
    catalogos.forEach(element => {
        let catalogoNome = element.title != null ? (element.title).replace(/(^\w{1})|(\s+\w{1})/g, letra => letra.toUpperCase()) : null
        let catalogoId = element.id
        let catalogoData = element.creation_date
        let image_id = element.image_id

        let linha = document.createElement('div')
        linha.className = 'linha'

        let data = document.createElement('div')
        data.className = 'linha-data'
        data.innerHTML = catalogoData

        let nome = document.createElement('div')
        nome.className = 'linha-nome'
        nome.innerHTML = catalogoNome

        //Botão visualizar
        let visualizar = document.createElement('div')
        visualizar.className = 'linha-bt'
        let visualizarBt = document.createElement('button')
        visualizarBt.type = 'button'
        visualizarBt.className = 'btn btn-sm btn-warning linha-bt-bt'
        visualizarBt.innerHTML = 'Abrir'
        visualizarBt.addEventListener('click', () => {
            window.location.href = `/pdfservice/pdfview/${image_id}.pdf`
        })
        visualizar.appendChild(visualizarBt)

        // Botão Baixar PDF
        let baixarPDF = document.createElement('div')
        baixarPDF.className = 'linha-bt'

        let baixarPDFBt = document.createElement('button')
        baixarPDFBt.type = 'button'
        baixarPDFBt.className = 'btn btn-sm btn-primary linha-bt-bt'
        baixarPDFBt.innerHTML = 'Baixar PDF'
        baixarPDFBt.addEventListener('click', () => {
            window.location.href = `/pdfservice/painel-administrativo/lista-de-catalogos?filter=downloadpdf&arg=${image_id}.pdf`
        })
        baixarPDF.appendChild(baixarPDFBt)
        
        // Botão Baixar PPTX
        let baixarPPTX = document.createElement('div')
        baixarPPTX.className = 'linha-bt'

        let baixarPPTXBt = document.createElement('button')
        baixarPPTXBt.type = 'button'
        baixarPPTXBt.className = 'btn btn-sm btn-info linha-bt-bt'
        baixarPPTXBt.innerHTML = 'Baixar PPTX'
        baixarPPTXBt.addEventListener('click', () => {
            window.location.href = `/pdfservice/painel-administrativo/lista-de-catalogos?filter=downloadpptx&arg=${image_id}.pptx`
        })
        baixarPPTX.appendChild(baixarPPTXBt)
        
        // Botão Excluir
        let excluir = document.createElement('div')
        excluir.className = 'linha-bt'

        let excluirBt = document.createElement('button')
        excluirBt.type = 'button'
        excluirBt.className = 'btn btn-sm btn-secondary linha-bt-bt'
        excluirBt.innerHTML = 'Excluir'
        excluirBt.addEventListener('click', () => {
            $(`#excluir${catalogoId}`).modal('show')
        })
        excluir.appendChild(excluirBt)
        
        let excluirModal = document.createElement('div')
        excluirModal.className = 'modal'
        excluirModal.classList.add('fade')
        excluirModal.id = `excluir${catalogoId}`
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
                Após a exclusão, todo o cadastro de ${nome.innerHTML} será apagado.
                </div>
                <form action="/pdfservice/painel-administrativo/lista-de-catalogos" method="POST">
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <input type="hidden" name="tipo" value="excluir">
                        <input type="hidden" name="id" value="${catalogoId}">
                        <button type="submit" class="btn btn-warning">Confirmar</button>
                    </div>
                </form>
            </div>
        </div>
        `
        excluir.appendChild(excluirModal)
        
        linha.appendChild(data)
        linha.appendChild(nome)
        linha.appendChild(visualizar)
        linha.appendChild(baixarPDF)
        linha.appendChild(baixarPPTX)
        linha.appendChild(excluir)
        lista.appendChild(linha)
    })
}

window.onload = function() {
    carregarLista()
} 