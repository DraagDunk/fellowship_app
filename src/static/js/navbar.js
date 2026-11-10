function menuFunction() {
  let navBar = document.getElementById("navigation");
  let homeLink = document.getElementById("home-link");
  if (navBar.style.display === "block") {
    navBar.style.display = "none";
    homeLink.classList.add("narrow");
  } else {
    navBar.style.display = "block";
    homeLink.classList.remove("narrow");
  }
}

function closeMenu() {
  let navBar = document.getElementById("navigation");
  let homeLink = document.getElementById("home-link");
  if (navBar.style.display === "block") {
    navBar.style.display = "none";
    homeLink.classList.add("narrow");
  }
}

function topnavCloseEvent() {
  const topnav = document.getElementById("topnav");
  document.addEventListener("click", (e) => {
    const clickTarget = e.target;
    if (!topnav.contains(clickTarget)) {
      closeMenu();
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  topnavCloseEvent();
  let topnavButtons = document.querySelectorAll(".topnav a");
  topnavButtons.forEach((e) => {
    if (e.id !== "burger") {
      e.addEventListener("click", closeMenu);
    }
  });
});
