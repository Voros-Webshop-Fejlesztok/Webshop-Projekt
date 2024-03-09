function toggleCheckbox() {
    var checkbox = document.getElementById('digital');
    checkbox.value = checkbox.checked ? 'true' : 'false';
}

var toggleFilter = document.getElementById("toggleFilter");
var moreFilter = document.getElementById("moreFilter");
var resetFilter = document.getElementById("resetFilter");
var checkbox = document.getElementById("digital");

// Az oldal betöltésekor ellenőrizd a cookie-t
window.onload = function() {
    // Ellenőrizd, hogy van-e tárolt érték a cookie-ben
    var isFilterHidden = getCookie("isFilterHidden");

    // Ha nincs tárolt érték, alapértelmezetten állítsd false-ra
    if (isFilterHidden === null) {
        isFilterHidden = "false";
    }

    // Alkalmazd a toggleFilter elemre az érték alapján
    toggleFilter.classList.toggle("hidden", isFilterHidden === "true");

    // Ellenőrizd, hogy van-e tárolt érték a filterData cookie-ben
    var filterData = getFilterDataFromCookie();

    // Alkalmazd az értékeket a megfelelő inputok és selectek elemekre
    applyFilterData(filterData);

    // Ellenőrizd, hogy van-e tárolt érték a checkbox cookie-ben
    var isDigitalChecked = getCookie("isDigitalChecked");

    // Ha nincs tárolt érték, alapértelmezetten állítsd false-ra
    if (isDigitalChecked === null) {
        isDigitalChecked = "false";
    }

    // Alkalmazd a checkbox állapotára az érték alapján
    checkbox.checked = isDigitalChecked === "true";

    // Állapotváltozás eseménykezelője
    checkbox.addEventListener("change", function() {
        // Cookie értékének frissítése
        setCookie("isDigitalChecked", checkbox.checked.toString(), 1);
        // Digitális adat mentése
        saveFilterData();
    });
};

// Minden változás esetén mentse az adatokat a cookie-ba
function saveFilterData() {
    var filterData = {
        ratingMin: document.getElementById("ratingMin").value,
        ratingMax: document.getElementById("ratingMax").value,
        priceMin: document.getElementById("priceMin").value,
        priceMax: document.getElementById("priceMax").value,
        inputBrand: document.getElementById("inputBrand").value,
        inputCategory: document.getElementById("inputCategory").value,
        pname: document.getElementById("pname").value,
        digital: document.getElementById("digital").value  // Digitális adat hozzáadva
    };

    // Állapot mentése a cookie-ba
    setFilterDataToCookie(filterData);
}

// Gomb eseménykezelők hozzáadása
moreFilter.addEventListener("click", function() {
    // Cookie értékének megváltoztatása
    var isFilterHidden = toggleFilter.classList.toggle("hidden");

    // Állapot mentése a cookie-ba
    setCookie("isFilterHidden", isFilterHidden.toString(), 1);

    // Adatok mentése
    saveFilterData();
});

resetFilter.addEventListener("click", function() {
    // Törölje az összes cookie-t, kivéve az isFilterHidden-t és isDigitalChecked-et
    document.cookie.split(";").forEach(function(cookie) {
        var trimmedCookie = cookie.trim();
        if (!(trimmedCookie.startsWith("isFilterHidden") || trimmedCookie.startsWith("isDigitalChecked"))) {
            var cookieName = trimmedCookie.split("=")[0];
            document.cookie = cookieName + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        }
    });

    // Állítsa a digitális értéket false-ra
    document.getElementById('digital').value = 'false';
    // Állítsa a checkbox állapotát false-ra
    document.getElementById('digital').checked = false;
    // Állítsa az isDigitalChecked cookie értékét false-ra
    setCookie("isDigitalChecked", "false", 1);

    // Törölje az input mezők értékeit
    var inputIdsToPreserve = ["ratingMin", "ratingMax", "priceMin", "priceMax", "inputBrand", "inputCategory", "pname"];
    inputIdsToPreserve.forEach(function(inputId) {
        document.getElementById(inputId).value = "";
    });
});

// Input és select mezők eseménykezelője
document.querySelectorAll("#ratingMin, #ratingMax, #priceMin, #priceMax, #inputBrand, #inputCategory, #pname").forEach(function(element) {
    element.addEventListener("input", function() {
        // Adatok mentése
        saveFilterData();
    });
});

// Cookie-k létrehozása és lekérdezése
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(nameEQ) === 0) {
            return cookie.substring(nameEQ.length, cookie.length);
        }
    }
    return null;
}

// Funkció az értékek alkalmazására az inputok és selectek elemekre
function applyFilterData(filterData) {
    document.getElementById("ratingMin").value = filterData.ratingMin || "";
    document.getElementById("ratingMax").value = filterData.ratingMax || "";
    document.getElementById("priceMin").value = filterData.priceMin || "";
    document.getElementById("priceMax").value = filterData.priceMax || "";
    document.getElementById("inputBrand").value = filterData.inputBrand || "";
    document.getElementById("inputCategory").value = filterData.inputCategory || "";
    document.getElementById("pname").value = filterData.pname || "";
    // Digitális adat alkalmazása
    document.getElementById("digital").value = filterData.digital || "";

    // Az input mezők értékeinek beállítása
    saveFilterData();
}

// Funkció az értékek mentésére a cookie-ba
function setFilterDataToCookie(filterData) {
    setCookie("filterData", JSON.stringify(filterData), 1);
}

// Funkció az értékek lekérdezésére a cookie-ból
function getFilterDataFromCookie() {
    return JSON.parse(getCookie("filterData")) || {};
}
