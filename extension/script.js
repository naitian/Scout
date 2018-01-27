const videoPlayer = document.querySelector('#movie_player > div.html5-video-container > video');

const init = () => {
    document.head.innerHTML += '<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">';
};

const toggleButtonSearch = () => {
    const input = document.querySelector('#scope-search > input');
    const button = document.querySelector('#scope-search > button');
    input.classList.toggle('active');
    button.classList.toggle('active');
    input.focus();
};

const filter = (term, response) => {
    return response(['hello', 'goodbye']);
};

const suggest = (e) => {
    term = e.target.value;
    console.log(term);
    suggestions = [];

    if (term) {
        suggestions = [term];
    }

    suggestions_output = document.querySelector('#scope-search #search-suggestions');
    if (suggestions.length > 0) {
        suggestions_output.classList.remove('empty');
        e.target.classList.add('suggestions');
        suggestions_output.innerText = term;
    } else {
        suggestions_output.classList.add('empty');
        e.target.classList.remove('suggestions');
        suggestions_output.innerText = '';
    }
};

const addButton = () => {
    console.log('adding button');
    const container = document.querySelector('#top');
    const scopeContainer = document.createElement('div');

    scopeContainer.id = 'scope-search';
    scopeContainer.innerHTML = `
        <button><i class="material-icons">search</i></button>
        <input type="text" id="search-input" />
        <div id="search-suggestions" class="empty"></div>
    `;

    let button = scopeContainer.querySelector('button');
    button.addEventListener('click', toggleButtonSearch);

    let input = scopeContainer.querySelector('#scope-search > #search-input');
    input.addEventListener('keyup', suggest);

    container.insertBefore(scopeContainer, container.children[1]);
};

const tryInit = () => {
    var poll = window.setInterval(() => {
        if (document.querySelector('#top')) {
            window.clearInterval(poll);
            init();
            addButton();
        }
    }, 100);
};

tryInit();

// document.body.onload = () => {
//     init();
//     addButton();
// };
