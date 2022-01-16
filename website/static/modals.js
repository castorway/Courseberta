var showModalDiv = document.getElementById("showModalDiv");
var modalId = showModalDiv.getAttribute("data-bs-name");

console.log("show_modal: " + modalId);

if (modalId != "") {
  var myModal = new bootstrap.Modal(document.getElementById(modalId));
  myModal.show();

  console.log("Showing modal " + modalId);
} else {
  console.log("No modal to show.");
}
