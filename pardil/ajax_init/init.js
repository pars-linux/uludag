window.onload = init;

init_functions = new Array();

function add_init(f) {
  init_functions[init_functions.length] = f;
}

function init() {

  for (var i = 0; i < init_functions.length; i++) {
    eval(init_functions[i] + '()')
  }

  document.getElementById('container').style.display = 'block';
}
