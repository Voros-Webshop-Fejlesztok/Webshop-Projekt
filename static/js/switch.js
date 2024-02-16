// Ellenőrzi, hogy van-e már beállítva dark mód
const isDarkMode = localStorage.getItem('darkMode') === 'enabled';
const body = document.querySelector('body');
const sidebar = body.querySelector('.sidebar');
const toggle = body.querySelector('.toggle');
const modeSwitch = body.querySelector('.toggle-switch');
const modeText = body.querySelector('.mode-text');

// Beállítja az oldal színét a tárolt beállításnak megfelelően
if (isDarkMode) {
    body.classList.add('dark');
    modeText.innerText = 'Világos mód';
    var path = window.location.pathname;
        if (path == "/store/") {
            document.getElementById('lightStore').classList.add('hidden')
            document.getElementById('darkStore').classList.remove('hidden')
        }
}

// Dark mód váltásának figyelése és tárolása
modeSwitch.addEventListener('click', () => {
    body.classList.toggle('dark');
    const currentMode = body.classList.contains('dark') ? 'enabled' : 'disabled';
    localStorage.setItem('darkMode', currentMode);

    if (body.classList.contains('dark')) {
        modeText.innerText = 'Világos mód';
        
        var path = window.location.pathname;
        if (path == "/store/") {
            document.getElementById('lightStore').classList.add('hidden')
            document.getElementById('darkStore').classList.remove('hidden')
        }


    } else {
        modeText.innerText = 'Sötét mód';
        
        var path = window.location.pathname;
        if (path == "/store/") {
            document.getElementById('lightStore').classList.remove('hidden')
            document.getElementById('darkStore').classList.add('hidden')
        }

    }
});

// Sidebar toggle eseményfigyelő
toggle.addEventListener('click', () => {
    sidebar.classList.toggle('close')
});