/* Set the initial width of the left navigation panel. */
function navSet() {
    document.getElementById("sidenav").style.width = "250px";
    document.getElementById("main").style.marginLeft = "270px";
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
    marginNew = widthNew + 20;
    marginNew = marginNew + "px";
    widthNew = widthNew + "px";
    document.getElementById("sidenav").style.width = widthNew;
    document.getElementById("main").style.marginLeft = marginNew;
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
    marginNew = widthNew + 20;
    marginNew = marginNew + "px";
    widthNew = widthNew + "px";
    document.getElementById("sidenav").style.width = widthNew;
    document.getElementById("main").style.marginLeft = marginNew;
}
