// AJAX button declarations
const ajaxButton = document.getElementById("button")
const ajaxDiv = document.getElementById("ajax_div")
const ajaxP = document.getElementById("ajax_p")
const inputField = document.getElementById('input')
const table = document.getElementById('table')
// modal declarations
const modalDiv = document.getElementById('modal_div')
const modalButton = document.getElementById('modal_button')
const modalClose = document.getElementsByClassName('modal_close')[0]

// modals code
modalButton.onclick = function () {
    modalDiv.style.display = "block";
}

modalClose.onclick = function () {
    modalDiv.style.display = "none"
}

window.onclick = function(event) {
    if (event.target == modalDiv) {
        modalDiv.style.display = "none"
        ajaxP.innerText = ''
    }

}

// Ajax button code - search by rating
ajaxButton.addEventListener('click', loadData);

function loadData() {
    fetch('/by_actor/' + inputField.value)
        .then(response => response.json())
        .then(response => {
            let characters = '<strong>Actor name  |  character name | show  |  show release year</strong></br></br>'
            for (let i = 0; i < response.length; i++) {
                characters += (response[i]['name'] + ' | ' + response[i]['character_name'] + ' | ' + response[i]['title'] + ' | ' + response[i]['to_char'] + '</br></br>')
            }
            ajaxP.innerHTML = characters
            inputField.value = ''
        })
}



// ajaxButtonRating.addEventListener('click', loadDataRating);
//
// function loadDataRating() {
//     fetch('/by_rating/' + inputField.value)
//         .then(response => response.json())
//         .then(response => {
//             let titles = ''
//             for (let i = 0; i < response.length; i++) {
//                 titles += response[i]['title'] + ', '
//             }
//             ajaxP.innerText = titles
//             inputField.value = ''
//         })
// }




