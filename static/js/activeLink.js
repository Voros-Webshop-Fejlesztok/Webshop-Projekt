document.addEventListener("DOMContentLoaded", function () {
var currentPath = window.location.pathname;
var links = document.querySelectorAll("#menu-links a");
	
links.forEach(function (link) {
	if (link.getAttribute("href") === currentPath) {
		link.classList.add("active");
	    }
	});
});