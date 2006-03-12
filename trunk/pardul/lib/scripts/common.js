
function tV(el, src) {
    var v = el.style.display == "block";
    var str = src.innerHTML;
    el.style.display = v ? "none" : "block";
    src.innerHTML = v ? str.replace(/up/, "down") : str.replace(/down/, "up");
}