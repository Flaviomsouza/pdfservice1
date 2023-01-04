let novoCatalogo = document.querySelector('#novo-catalogo')
novoCatalogo.addEventListener('click', () => {
    window.location.href = '/pdfservice/painel-administrativo/novo-catalogo'
})
let listaDeCatalogos = document.querySelector('#lista-de-catalogos')
listaDeCatalogos.addEventListener('click', () => {
    window.location.href = '/pdfservice/painel-administrativo/lista-de-catalogos'
})
let colaboradores = document.querySelector('#colaboradores')
colaboradores.addEventListener('click', () => {
    window.location.href = '/pdfservice/painel-administrativo/colaboradores'
})