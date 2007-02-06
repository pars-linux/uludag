
function tv(el, src) {
    var v = el.style.display == "block";
    var str = src.innerHTML;
    el.style.display = v ? "none" : "block";
    src.innerHTML = v ? str.replace(/2/, "1") : str.replace(/1/, "2");
}