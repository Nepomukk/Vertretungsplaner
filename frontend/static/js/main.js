function fpRemoveAbsenceLesson(element) {
    let elements = document.querySelectorAll('.fp-absence-lessons .input-container.fp-absence-grid');
    if (elements.length > 1) {
        element.closest('.input-container.fp-absence-grid').remove();
    } else {
        let inputs = element.closest('.input-container.fp-absence-grid').querySelectorAll('input');
        for (let input of inputs) {
            input.value = '';
        }
    }
}

function fpAddAbsenceLesson() {
    let elements = document.querySelectorAll('.fp-absence-lessons .input-container.fp-absence-grid');
    elements[elements.length - 1].after(elements[elements.length - 1].cloneNode(true));
}