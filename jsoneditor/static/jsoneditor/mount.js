
document.addEventListener('DOMContentLoaded', function () {
  var editorElements = document.querySelectorAll('div.for_jsoneditor');

  for (var i=0; i<editorElements.length; i++) {
    var elem = editorElements[i];
    var valueElem = document.getElementById(
          elem.id.substr(0, elem.id.length - '_jsoneditor'.length))

    if (!valueElem) throw new Error();

    var editor = new JSONEditor(elem, {
      schema: JSON.parse(elem.dataset.schema),
      theme: 'bootstrap3',
      iconlib: 'bootstrap3'
    })

    var initialValue = valueElem.value;
    try {
      editor.setValue(JSON.parse(initialValue));
    } catch (err) {
      console.error("Could not parse initial value")
      console.error(initialValue)
    }

    // Traverse ancestors to find form
    var formElement = elem;
    while (formElement.tagName !== 'FORM')
      formElement = formElement.parentNode

    formElement.addEventListener('submit', function () {
      elem.parentNode.removeChild(elem);
    })


    var timeout = null;
    editor.on('change', function () {
      function update() {
        console.log(valueElem);
        valueElem.value = JSON.stringify(editor.getValue());
      }

      if (timeout === null) {
        update();
      }
      else {
        timeout = setTimeout(function() {
          update();
          timeout = null;
        }, 1000)
      }
    })
  }
});
