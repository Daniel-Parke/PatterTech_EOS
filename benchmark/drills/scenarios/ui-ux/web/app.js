// Form checks. Runs on submit, puts a message next to the field.

(function () {
  var form = document.getElementById('leak');
  if (!form) {
    return;
  }

  function clear() {
    var old = form.querySelectorAll('.error');
    for (var i = 0; i < old.length; i++) {
      old[i].parentNode.removeChild(old[i]);
    }
  }

  function complain(field, text) {
    var span = document.createElement('span');
    span.className = 'error';
    span.textContent = text;
    field.parentNode.insertBefore(span, field.nextSibling);
  }

  form.addEventListener('submit', function (event) {
    clear();
    var bad = false;
    var postcode = document.getElementById('postcode');
    var where = document.getElementById('where');
    var phone = document.getElementById('phone');

    if (!postcode.value.trim()) {
      complain(postcode, 'Enter a postcode');
      bad = true;
    }
    if (!where.value.trim()) {
      complain(where, 'Tell us what you can see');
      bad = true;
    }
    if (!phone.value.trim()) {
      complain(phone, 'Enter a phone number');
      bad = true;
    }
    if (bad) {
      event.preventDefault();
    }
  });
}());
