const videoPlayer = document.querySelector('#movie_player > div.html5-video-container > video');

const init = () => {
    document.head.innerHTML += '<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">';
};

const addButton = () => {
    console.log('adding button');
    const container = document.querySelector('#top');
    const scopeContainer = document.createElement('div');

    console.log(container);

    scopeContainer.innerHTML = `
        <button><i class="material-icons">search</i></button>
    `;

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
