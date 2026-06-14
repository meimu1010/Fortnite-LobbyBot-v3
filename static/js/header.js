const HREFS = [
    '/',
    '/config-editor',
    '/commands-editor',
    '/custom-commands-editor',
    '/replies-editor',
    '/boot-switch',
    '/clients-viewer'
];

const headerList = document.getElementById('header-list');
headerList.classList.add('pc-header-list');

HREFS.forEach(href => {
    const li = document.createElement('li');
    li.className = 'header-item';

    if (href == location.pathname) {
        const p = document.createElement('p');
        p.textContent = texts[href];
        li.appendChild(p);
    } else {
        const a = document.createElement('a');
        a.href = href;
        a.textContent = texts[href];
        li.appendChild(a);
    }

    headerList.appendChild(li);
});

document.getElementById('header-button').addEventListener('click', function () {
    this.classList.toggle('header-button-open');
    headerList.classList.toggle('header-list-open');
});

const logo = document.getElementById('pc-logo');
const headerButton = document.getElementById('header-button');

function fitSize() {
    const headerWidth = logo.clientWidth + headerList.clientWidth;
    const windowWidth = window.innerWidth - 20;

    headerList.classList.toggle('phone-header-list', headerWidth > windowWidth);
    headerList.classList.toggle('pc-header-list', headerWidth <= windowWidth);
    headerButton.classList.toggle('header-button', headerWidth > windowWidth);
    headerButton.classList.remove('header-button-open');
    headerList.classList.remove('header-list-open');
}

fitSize();

window.addEventListener('resize', fitSize);