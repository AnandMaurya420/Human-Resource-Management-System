    const toggleBtn = document.getElementById('themeToggle');
    const body = document.body;

    const currentTheme = localStorage.getItem('theme') || 'dark';
    body.classList.add(currentTheme);
    toggleBtn.textContent = currentTheme === 'dark' ? '🌞 Light Mode' : '🌙 Dark Mode';

    toggleBtn.addEventListener('click', () => {
      body.classList.toggle('dark');
      body.classList.toggle('light');
      const theme = body.classList.contains('dark') ? 'dark' : 'light';
      localStorage.setItem('theme', theme);
      toggleBtn.textContent = theme === 'dark' ? '🌞 Light Mode' : '🌙 Dark Mode';
    });