let novoCatalogo = document.querySelector('#novo-book')
novoCatalogo.addEventListener('click', () => {
    window.location.href = '/pdfservice/painel-administrativo/novo-book'
})
let listaDeCatalogos = document.querySelector('#lista-de-books')
listaDeCatalogos.addEventListener('click', () => {
    window.location.href = '/pdfservice/painel-administrativo/lista-de-books'
})
let colaboradores = document.querySelector('#colaboradores')
colaboradores.addEventListener('click', () => {
    window.location.href = '/pdfservice/painel-administrativo/colaboradores'
})