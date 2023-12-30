const answers = document.querySelectorAll('.answer');
const submitButton = document.getElementById('submit');
const flagButton = document.getElementById('flag');
const flagIncorrectButton = document.getElementById('flagIncorrect');

answers.forEach(answer => {
    answer.addEventListener('click', () => {
        answers.forEach(a => a.classList.remove('selected'));
        answer.classList.add('selected');
    });
});

submitButton.addEventListener('click', () => {
    const selectedAnswer = document.querySelector('.answer.selected');
    document.getElementById('hiddenInput').value = selectedAnswer.innerText;
    document.getElementById('hiddenForm').submit();
});

flagButton.addEventListener('click', () => {
    alert('Question flagged for review.');
    document.getElementById('hiddenInput').name = "flag"
    document.getElementById('hiddenInput').value = "review";
    document.getElementById('hiddenForm').submit();
});

flagIncorrectButton.addEventListener('click', () => {
    alert('Question flagged as incorrect.');
    document.getElementById('hiddenInput').name = "flag"
    document.getElementById('hiddenInput').value = "incorrect";
    document.getElementById('hiddenForm').submit();
});