var toggleFilter = document.getElementById("toggleFilter");
var moreFilter = document.getElementById("moreFilter");

// Gomb eseménykezelő hozzáadása
moreFilter.addEventListener("click", function() {
    toggleFilter.classList.toggle("hidden");
});