const moreButton = document.getElementById('more');
const newButton = document.getElementById('new');
const againButton = document.getElementById('again');

moreButton.addEventListener('click', () => {
    document.getElementById('hiddenInput').value = "more";
    document.getElementById('hiddenForm').submit();
});

newButton.addEventListener('click', () => {
    document.getElementById('hiddenInput').value = "new";
    document.getElementById('hiddenForm').submit();
});

againButton.addEventListener('click', () => {
    document.getElementById('hiddenInput').value = "again";
    document.getElementById('hiddenForm').submit();
});
