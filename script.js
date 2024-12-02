async function sendData(url, data, method = 'POST', resultDivId = null) {
    const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    if (resultDivId) {
        document.getElementById(resultDivId).innerHTML = result.message;
    }
}

function addAuthor() {
    const name = document.getElementById('author-name').value;
    sendData('/add_author', { name: name }, 'POST', 'add-author-result');
}

function addBook() {
    const title = document.getElementById('book-title').value;
    const year = document.getElementById('book-year').value;
    sendData('/add_book', { title: title, year: year }, 'POST', 'add-book-result');
}

function linkAuthorBook() {
    const author = document.getElementById('link-author').value;
    const book = document.getElementById('link-book').value;
    sendData('/link_author_book', { author: author, book: book }, 'POST', 'link-author-book-result');
}

async function getBooksByAuthor() {
    const author = document.getElementById('search-author').value;
    const response = await fetch(`/get_books_by_author/${author}`);
    const result = await response.json();
    const resultDiv = document.getElementById('books-by-author-result');
    if (result.message) {
        resultDiv.innerHTML = result.message;
    } else {
        resultDiv.innerHTML = result.map(book => `${book.title} (${book.year})`).join('<br>');
    }
}

function deleteAuthor() {
    const name = document.getElementById('delete-author-name').value;
    sendData('/delete_author', { name: name }, 'DELETE', 'delete-author-result');
}

function deleteBook() {
    const title = document.getElementById('delete-book-title').value;
    sendData('/delete_book', { title: title }, 'DELETE', 'delete-book-result');
}

async function getAllAuthors() {
    const response = await fetch('/get_all_authors');
    const result = await response.json();
    const resultDiv = document.getElementById('authors-result');
    if (result.message) {
        resultDiv.innerHTML = result.message;
    } else {
        resultDiv.innerHTML = result.map(author => author.name).join('<br>');
    }
}

async function getAllBooks() {
    const response = await fetch('/get_all_books');
    const result = await response.json();
    const resultDiv = document.getElementById('all-books-result');
    if (result.message) {
        resultDiv.innerHTML = result.message;
    } else {
        resultDiv.innerHTML = result.map(book => `${book.title} (${book.year})`).join('<br>');
    }
}

async function getAuthorsByBook() {
    const book = document.getElementById('search-book').value;
    const response = await fetch(`/get_authors_by_book/${book}`);
    const result = await response.json();
    const resultDiv = document.getElementById('authors-by-book-result');
    if (result.message) {
        resultDiv.innerHTML = result.message;
    } else {
        resultDiv.innerHTML = result.map(author => author.name).join('<br>');
    }
}

async function getBooksByYearRange() {
    const startYear = document.getElementById('start-year').value;
    const endYear = document.getElementById('end-year').value;
    const response = await fetch(`/get_books_by_year_range?start=${startYear}&end=${endYear}`);
    const result = await response.json();
    const resultDiv = document.getElementById('books-by-year-range-result');
    if (result.message) {
        resultDiv.innerHTML = result.message;
    } else {
        resultDiv.innerHTML = result.map(book => `${book.title} (${book.year})`).join('<br>');
    }
}

async function findShortestPath() {
    const author1 = document.getElementById('author1').value;
    const author2 = document.getElementById('author2').value;
    const response = await fetch(`/find_shortest_path?author1=${author1}&author2=${author2}`);
    const result = await response.json();
    if (result.message) {
        showResultWindow(result.message);
    } else {
        const formattedPath = formatPath(result.path);
        showResultWindow(formattedPath);
    }
}

async function fetchAuthors() {
    const response = await fetch('/get_all_authors');
    const authors = await response.json();
    const authorList = document.getElementById('author-list');
    authorList.innerHTML = authors.map(author => `<option value="${author.name}">`).join('');
}

async function fetchBooks() {
    const response = await fetch('/get_all_books');
    const books = await response.json();
    const bookList = document.getElementById('book-list');
    bookList.innerHTML = books.map(book => `<option value="${book.title}">`).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    fetchAuthors();
    fetchBooks();
});