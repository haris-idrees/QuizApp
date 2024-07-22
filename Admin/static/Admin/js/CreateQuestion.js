
document.addEventListener('DOMContentLoaded', function() {
    let optionForms = document.querySelectorAll(".option-form");
    let container = document.querySelector("#options_formset");
    let addButton = document.querySelector("#add-option");
    let totalForms = document.querySelector("#id_options-TOTAL_FORMS");

    if (!totalForms) {
        console.error("Element with id 'id_options-TOTAL_FORMS' not found.");
        return;
    }

    let formNum = optionForms.length - 1;
    addButton.addEventListener('click', addForm);

    function addForm(e) {
        e.preventDefault();

        let newForm = optionForms[0].cloneNode(true);
        let formRegex = /options-(\d+)-/g;

        formNum++;
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `options-${formNum}-`);

        // Update the ID and name attributes of the new form fields
        let formFields = newForm.querySelectorAll('input, select, textarea, label');
        formFields.forEach(function(field) {
            if (field.id) {
                console.log(`Updating field id from ${field.id} to ${field.id.replace(formRegex, `options-${formNum}-`)}`);
                field.id = field.id.replace(formRegex, `options-${formNum}-`);
            }
            if (field.name) {
                console.log(`Updating field name from ${field.name} to ${field.name.replace(formRegex, `options-${formNum}-`)}`);
                field.name = field.name.replace(formRegex, `options-${formNum}-`);
            }
            if (field.htmlFor) { // Update label 'for' attributes
                console.log(`Updating label for from ${field.htmlFor} to ${field.htmlFor.replace(formRegex, `options-${formNum}-`)}`);
                field.htmlFor = field.htmlFor.replace(formRegex, `options-${formNum}-`);
            }
        });

        // Add remove button event listener
        newForm.querySelector('.remove-option').addEventListener('click', removeForm);

        container.appendChild(newForm);

        totalForms.setAttribute('value', `${formNum + 1}`);
    }

    function removeForm(e) {
        e.preventDefault();
        let formToRemove = e.target.closest('.option-form');
        formToRemove.remove();

        // Update total forms count
        let currentForms = document.querySelectorAll('.option-form').length;
        totalForms.setAttribute('value', `${currentForms}`);
    }

    // Add remove event listeners to initial forms
    optionForms.forEach(function(form) {
        form.querySelector('.remove-option').addEventListener('click', removeForm);
    });
});


