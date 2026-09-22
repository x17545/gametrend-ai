const themeToggleBtn =
  document.getElementById("themeToggleBtn");

const savedTheme =
  localStorage.getItem("gametrend-theme");

if (savedTheme === "light") {
  document.body.classList.add("light-theme");
}

function updateThemeButton() {
  const isLight =
    document.body.classList.contains("light-theme");

  themeToggleBtn.textContent =
    isLight
      ? "🌙 DARK MODE"
      : "☀ LIGHT MODE";
}

themeToggleBtn.addEventListener("click", () => {
  document.body.classList.toggle("light-theme");

  const isLight =
    document.body.classList.contains("light-theme");

  localStorage.setItem(
    "gametrend-theme",
    isLight ? "light" : "dark"
  );

  updateThemeButton();
});

updateThemeButton();