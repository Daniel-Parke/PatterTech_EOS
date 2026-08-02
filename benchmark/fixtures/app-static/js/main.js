// Progressive enhancement: load testimonials into the home page.
// Renders with createElement and textContent only, never innerHTML,
// so testimonial text is always treated as plain data.

(function () {
  "use strict";

  var container = document.getElementById("testimonials");
  if (!container || typeof fetch !== "function") {
    return;
  }

  fetch("data/testimonials.json")
    .then(function (response) {
      if (!response.ok) {
        throw new Error("bad status " + response.status);
      }
      return response.json();
    })
    .then(function (items) {
      items.forEach(function (item) {
        var block = document.createElement("blockquote");
        block.className = "testimonial";

        var text = document.createElement("p");
        text.textContent = item.text;

        var cite = document.createElement("cite");
        cite.textContent = item.name + ", " + item.area;

        block.appendChild(text);
        block.appendChild(cite);
        container.appendChild(block);
      });
    })
    .catch(function () {
      // Fetch is unavailable on file:// or the JSON is missing.
      // Fail silently, the page works without testimonials.
    });
})();
