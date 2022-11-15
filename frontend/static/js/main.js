

function showMessages(){

    var toggleBox = document.getElementById('toggleBox')
    if(toggleBox.classList.contains('hidden'))
    {
    toggleBox.classList.remove('hidden')
    else
    {
    toggleBox.classList.add('hidden')
    }
}