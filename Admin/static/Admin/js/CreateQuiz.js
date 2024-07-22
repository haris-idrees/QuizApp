
document.addEventListener('DOMContentLoaded', function() {
    let questionForms = document.querySelectorAll(".question-form");
    let questionContainer = document.querySelector("#questions_formset");
    let addQuestionButton = document.querySelector("#add-question");
    let totalQuestionForms = document.querySelector("#id_questions-TOTAL_FORMS");

    let option_field = document.querySelector('.option_input');
    console.log(option_field.name)

    let addOptionButton = document.querySelector('.add-option');
    addOptionButton.addEventListener('click', addOption)

    function addOption(button) {
        let questionForm = button.closest('.question-form');
        let optionContainer = questionForm.querySelector('#options-container');
        let optionFields = optionContainer.querySelectorAll('.option_input');
        let newField = optionFields[0].cloneNode(true);

        newField.value = '';

        optionContainer.appendChild(newField);
    }


    if (!totalQuestionForms) {
        console.error("Element with id 'id_questions-TOTAL_FORMS' not found.");
        return;
    }

    let questionFormNum = questionForms.length - 1;
    addQuestionButton.addEventListener('click', addQuestionForm);

    function addQuestionForm(e) {
        e.preventDefault();
        let newForm = questionForms[0].cloneNode(true);
        let formRegex = /questions-(\d+)-/g;

        questionFormNum++;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `questions-${questionFormNum}-`);

        let formFields = newForm.querySelectorAll('input, select, textarea, label');

        console.log('Question Fields')
        formFields.forEach(function(field) {
            if (field.id) {
                field.id = field.id.replace(formRegex, `questions-${questionFormNum}-`);
                console.log('field id', field.id, field.name)
            }
            if (field.name) {
                field.name = field.name.replace(formRegex, `questions-${questionFormNum}-`);
            }
            if (field.htmlFor) {
                field.htmlFor = field.htmlFor.replace(formRegex, `questions-${questionFormNum}-`);
            }
        });
        console.log('Question added')
        let optionContainer = newForm.querySelector('#options-container');
        optionContainer.innerHTML = '';

        let initialOptionField = document.createElement('div');
        initialOptionField.classList.add('option-group');
        initialOptionField.innerHTML = `
            <label for="option_text">Answer Option: </label>
            <input class="form-control option_input" type="text" name="questions-${questionFormNum}-option_text" id="${questionFormNum}_option_0">
        `;
    optionContainer.appendChild(initialOptionField);

        questionContainer.appendChild(newForm);
        totalQuestionForms.setAttribute('value', `${questionFormNum + 1}`);
    }

    questionContainer.addEventListener('click', function(e) {
    if (e.target && e.target.classList.contains('add-option')) {
            addOption(e.target);
        }
    });

});
