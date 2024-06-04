function load() {
    const isdark = localStorage.getItem("theme");
    if(isdark == "true") {
        document.getElementById("theme").setAttribute('data-theme', 'light');
    }
    else {
        document.getElementById("theme").setAttribute('data-theme', 'dark');
    }
}


function ChangeTheme () {
    const isdark = localStorage.getItem("theme");
    if(isdark == "true") {
        document.getElementById("theme").setAttribute('data-theme', 'dark');
        localStorage.setItem("theme", "false");
        
    }
    else {
        document.getElementById("theme").setAttribute('data-theme', 'light');
        localStorage.setItem("theme", "true");
    }
}