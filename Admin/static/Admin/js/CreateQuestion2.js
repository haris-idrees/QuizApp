document.addEventListener('DOMContentLoaded', function() {
    var questionTypeField = document.getElementById('id_question_type');
    var mcqOptions = document.getElementById('mcq-options');
    var tfOptions = document.getElementById('tf-options');
    var saOptions = document.getElementById('sa-options');

    function toggleOptions() {
        mcqOptions.style.display = 'none';
        tfOptions.style.display = 'none';
        saOptions.style.display = 'none';

        if (questionTypeField.value === 'MCQ') {
            mcqOptions.style.display = 'block';
        } else if (questionTypeField.value === 'TF') {
            tfOptions.style.display = 'block';
        } else if (questionTypeField.value === 'SA') {
            saOptions.style.display = 'block';
        }
    }

    questionTypeField.addEventListener('change', toggleOptions);
    toggleOptions();
});
