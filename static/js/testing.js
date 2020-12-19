const searchP = document.getElementById('search_p')
const searchInput = document.getElementById('search_input')
const searchButton = document.getElementById('search_button')
const searchTable = document.getElementById('search_table')
const searchH2 = document.getElementById('search_h2')

searchButton.addEventListener('click', LoadData);

function LoadData() {
    fetch('/data/testing/' + searchInput.value)
        .then(response => response.json())
        .then(response => {
            let actors = '<strong>Actor   |   Character   |   Show</strong></br></br>'
            for (let i = 0; i < response.length; i++) {
                actors += (response[i]['name'] + '   |   ' + response[i]['character_name'] + '   |   ' + response[i]['title'] + '</br></br>')
            }
            searchH2.innerText = 'Search result:'
            searchP.innerHTML = actors
            searchInput.value = ''
        })
}
