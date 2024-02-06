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
}

// Dark mód váltásának figyelése és tárolása
modeSwitch.addEventListener('click', () => {
    body.classList.toggle('dark');
    const currentMode = body.classList.contains('dark') ? 'enabled' : 'disabled';
    localStorage.setItem('darkMode', currentMode);

    if (body.classList.contains('dark')) {
        modeText.innerText = 'Világos mód';
    } else {
        modeText.innerText = 'Sötét mód';
    }
});

// Sidebar toggle eseményfigyelő
toggle.addEventListener('click', () => {
    sidebar.classList.toggle('close');
});
