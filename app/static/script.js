// Script personalizzati per AssoHUB
(function () {
    const THEME_STORAGE_KEY = 'theme';

    function applyTheme(theme) {
        const normalizedTheme = theme === 'dark' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', normalizedTheme);
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            const isDark = normalizedTheme === 'dark';
            toggleBtn.textContent = isDark ? 'Tema chiaro' : 'Tema scuro';
            toggleBtn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        const savedTheme = localStorage.getItem(THEME_STORAGE_KEY) || document.documentElement.getAttribute('data-theme') || 'light';
        applyTheme(savedTheme);

        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme');
                const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
                localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
                applyTheme(nextTheme);
            });
        }
    });
})();
