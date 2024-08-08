document.addEventListener("DOMContentLoaded", function () {
  var textarea = document.getElementById("content");
  var charCounter = document.getElementById("charCounter");

  textarea.addEventListener("input", function () {
    var currentLength = textarea.value.length;
    charCounter.textContent = currentLength + " / 500 characters";
  });
});
