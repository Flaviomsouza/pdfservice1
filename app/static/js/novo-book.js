var alertGenerate = function(parentElement, text) {
    let oldAlert = document.querySelector('#alert')
    let alertExists = parentElement.contains(oldAlert)
    console.log(alertExists)
    if (alertExists) {
        oldAlert.outerHTML = ''
    }

    let alert = document.createElement('div')
    alert.className = 'alert alert-warning alert-dismissible fade show'
    alert.role = 'alert'
    alert.id = 'alert'
    alert.innerHTML = `
        ${text}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `
    parentElement.insertAdjacentElement('afterbegin', alert)
}

var menu = document.querySelector('#menu')

let uploadOption = document.querySelector('#upload-option')
let uploadBtClickCheck = false
uploadOption.addEventListener('click', () => {
    let divInfo = document.querySelector('#info')
    if (uploadBtClickCheck == false) {
        let nomeBook = document.querySelector('#nome').value
        if (!nomeBook) {
            alertGenerate(menu, 'Escolha um nome para o novo book.')
            return
        }
        uploadBtClickCheck = true
        divInfo.innerHTML = ''
        

        let formFile = document.createElement('form')
        formFile.method = 'POST'
        formFile.action = '/pdfservice/painel-administrativo/novo-book'
        formFile.enctype = "multipart/form-data"

        let inputSection = document.createElement('div')
        inputSection.className = 'input-section'
    
        let inputNome = document.createElement('input')
        inputNome.type = 'hidden'
        inputNome.name = 'nome'
        inputNome.value = nomeBook
        
        let nomeCliente = document.querySelector('#cliente').value
        let inputCliente = document.createElement('input')
        inputCliente.type = 'hidden'
        inputCliente.name = 'cliente'
        inputCliente.value = nomeCliente
        
        let nomePessoa = document.querySelector('#pessoa').value
        let inputPessoa = document.createElement('input')
        inputPessoa.type = 'hidden'
        inputPessoa.name = 'pessoa'
        inputPessoa.value = nomePessoa
        
        let divInputFile = document.createElement('div')
        divInputFile.className = 'input-file'
        let inputFileLabel = document.createElement('p')
        inputFileLabel.innerHTML = 'Selecionar Arquivo'
        let inputFile = document.createElement('input')
        inputFile.type = 'file'
        inputFile.accept = '.xlsx, .csv, .xls'
        inputFile.name = 'input-file'
        inputFile.id = 'input-file'
        divInputFile.appendChild(inputFileLabel)
        divInputFile.appendChild(inputFile)
    
        let divInputButton = document.createElement('div')
        divInputButton.className = 'input-button'

        let modalInputButton = document.createElement('div')
        modalInputButton.className = 'modal fade'
        modalInputButton.id = 'staticBackdrop'
        modalInputButton.setAttribute('data-bs-backdrop', 'static')
        modalInputButton.setAttribute('data-bs-keyboard', 'false')
        modalInputButton.tabIndex = '-1'
        modalInputButton.setAttribute('aria-labelledby', 'staticBackdropLabel')
        modalInputButton.ariaHidden = true
        modalInputButton.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="staticBackdropLabel">Aguarde...</h5>
                </div>
                <div class="modal-body">
                    Fazendo o download das imagens e gerando os links e os documentos PDF e PPTX. Isso pode levar alguns minutos.
                    <div class="spinner-border text-warning" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            </div>
        </div>
        `
        
        let inputButton = document.createElement('button')
        inputButton.className = 'btn-dark btn'
        inputButton.innerHTML = 'Enviar'
        inputButton.addEventListener('click', () => {
            $('#staticBackdrop').modal('show')
        })
        divInputButton.appendChild(inputButton)
        divInputButton.appendChild(modalInputButton)
    
        inputSection.appendChild(divInputFile)
        inputSection.appendChild(divInputButton)
        formFile.appendChild(inputNome)
        formFile.appendChild(inputCliente)
        formFile.appendChild(inputPessoa)
        formFile.appendChild(inputSection)
        divInfo.appendChild(formFile)
    }
})