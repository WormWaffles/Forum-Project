let darkmode = localStorage.getItem("darkmode");
const darkmodeToggle = document.querySelector("#darkmode-toggle");

const enableDarkMode = () => {
    // 1. add the class "darkmode" to the body
    document.body.classList.add("darkmode");
    // 2. update darkmode in the localstorage
    localStorage.setItem("darkmode", "enabled");
};

const disableDarkMode = () => {
    // 1. remove the class "darkmode" to the body
    document.body.classList.remove("darkmode");
    // 2. update darkmode in the localstorage
    localStorage.setItem("darkmode", null);
};

// check if the user already visited and enabled darkmode
if (darkmode === "enabled") {
    enableDarkMode();
}

darkmodeToggle.addEventListener("click", () => {
    darkmode = localStorage.getItem("darkmode");
    if (darkmode !== "enabled") {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
});