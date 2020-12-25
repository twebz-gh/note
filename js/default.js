/* Set the initial width of the left navigation panel. */
function navSet() {
    document.getElementById("sidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

/* Increase the width of the left navigation panel. */
function navInc() {
    let widthIncrement = 50;
    let widthMaximum = 700;
    let widthCurrent = parseInt(document.getElementById("sidenav").style.width);
    let widthNew = widthCurrent + widthIncrement;
    if (widthNew > widthMaximum) {
        widthNew = widthMaximum;
    }
    widthNew = widthNew + "px";
    document.getElementById("sidenav").style.width = widthNew;
    document.getElementById("main").style.marginLeft = widthNew;
}

/* Decrease the width of the left navigation panel. */
function navDec() {
    let widthIncrement = 50;
    let widthMinimum = 100;
    let widthCurrent = parseInt(document.getElementById("sidenav").style.width);
    let widthNew = widthCurrent - widthIncrement;
    if (widthNew < widthMinimum) {
        widthNew = widthMinimum;
    }
    widthNew = widthNew + "px";
    document.getElementById("sidenav").style.width = widthNew;
    document.getElementById("main").style.marginLeft = widthNew;
}
