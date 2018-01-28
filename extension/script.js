const videoPlayer = document.querySelector('#movie_player > div.html5-video-container > video');

const init = () => {
    document.head.innerHTML += '<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">';
};

const runPipeline = (e) => {
    const button = document.querySelector('#scope-search > button');
    button.removeEventListener('click', runPipeline);
    button.disabled = true;

    console.log('Labels not cached. Running pipeline...')
    console.log(JSON.stringify({'url': youtube_url}))
    fetch('https://scope.naitian.org/process', {
        method: 'POST',
        headers: {
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
        },
        body: 'url=' + youtube_url
    });
}

const toggleButtonSearch = () => {
    const input = document.querySelector('#scope-search > input');
    const button = document.querySelector('#scope-search > button');
    input.classList.toggle('active');
    button.classList.toggle('active');

    if (!input.classList.contains('active')) {
        const sug = document.querySelector('#scope-search > #search-suggestions');
        sug.classList.add('empty');
        sug.innerHTML = '';
    }
    input.focus();
};

class FuzzySearch {
    constructor (fetched_keywords) {
        this.keywords = fetched_keywords;
        this.fuse = this.initFuse(this.keywords);
    }

    initFuse (keywords) {
        return new Fuse(keywords, {
            keys: ['keyword'],
            minMatchCharLength: 2,
            findAllMatches: false,
            threshold: 0.5
        });
    }

    search (term) {
        return this.fuse.search(term);
    }
}

const seek = (e) => {
    videoPlayer.currentTime = e.target.dataset.timestamp - 0.6;
};

const suggest = (e, fzsch) => {
    term = e.target.value;
    let suggestions = [];

    suggestions = fzsch.search(term);

    suggestions_output = document.querySelector('#scope-search #search-suggestions');
    if (suggestions.length > 0) {
        suggestions_output.classList.remove('empty');
        e.target.classList.add('suggestions');
        suggestions_output.innerHTML = '';
        for (var i = 0, len = suggestions.length; i < len; i++) {
            suggestions_output.innerHTML += `
                <div class="search-results">
                    ${suggestions[i].keyword}
                    <span class="timestamps">
                        ${suggestions[i].timestamps.map(val => `<a data-timestamp="${val}">${val}</a>`).join(' ')}
                    </span>
                </div>`;
        }
        // suggestions_output.innerText = suggestions;
    } else {
        suggestions_output.classList.add('empty');
        e.target.classList.remove('suggestions');
        suggestions_output.innerText = '';
    }
};

const addButton = () => {
    console.log('adding button');
    const container = document.querySelector('#top');
    const alertsContainer = document.querySelector('#container > #main');
    const alerts = document.querySelector('#main > #alerts');
    const scopeContainer = document.createElement('div');

    scopeContainer.id = 'scope-search';
    scopeContainer.innerHTML = `
        <button><i class="material-icons">search</i></button>
        <input type="text" id="search-input" />
        <div id="search-suggestions" class="empty"></div>
    `;

    let button = scopeContainer.querySelector('button');
    button.disabled = true;

    let input = scopeContainer.querySelector('#scope-search > #search-input');
    
    let first404 = true;
    let poll_aws = window.setInterval(() => {
        if(window.location.href.indexOf('&') == -1){
            youtube_url = window.location.href;
        } else {
            youtube_url = window.location.href.substring(0, window.location.href.indexOf('&'));
        }
        url = 'https://u1pzky3w1b.execute-api.us-east-1.amazonaws.com/v1?url=' + youtube_url
        fetch(url, {
            method: 'POST',
        }).then(function(response){
            if(response.status == 200){
                button.disabled = false;
                button.addEventListener('click', toggleButtonSearch);
                
                return response.json()
            } else if(first404) {
                first404 = false;
                button.disabled = false;
                button.addEventListener('click', runPipeline);
            }
        }).then(function(value){
            let fzsch = new FuzzySearch(value);
            input.addEventListener('keyup', function (e) {
                suggest(e, fzsch);
            });
        });
    }, 3000);

    let suggestions_output = scopeContainer.querySelector('#scope-search #search-suggestions');
    suggestions_output.addEventListener('click', function (e) {
        if (e.target && e.target.nodeName === 'A') {
            seek(e);
        }
    });

    alertsContainer.insertBefore(scopeContainer, alerts);
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
