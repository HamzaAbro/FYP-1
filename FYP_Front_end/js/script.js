
  const toggleBtn = document.getElementById("themeToggle");

  // Check if user already selected a theme (save in localStorage)
  if (localStorage.getItem("theme") === "light") {
    document.body.classList.add("light-theme");
    toggleBtn.textContent = "☀️ Light";
  }

  toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("light-theme");

    if (document.body.classList.contains("light-theme")) {
      toggleBtn.textContent = "☀️ Light";
      localStorage.setItem("theme", "light"); // remember choice
    } else {
      toggleBtn.textContent = "🌙 Dark";
      localStorage.setItem("theme", "dark");
    }
  });