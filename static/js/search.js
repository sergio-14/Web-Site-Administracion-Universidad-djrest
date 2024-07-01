function filterCards() {
    let query = document.getElementById('search').value;
    fetch(`?q=${query}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('users-container').innerHTML = data.html;
    });
}
