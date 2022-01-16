submit_button = document.querySelector(
    "#viewModal > div > div > div.modal-footer > button.btn.btn-primary"
);
modal_one = document.querySelector("#viewModal");
modal_two = document.querySelector("#selectPicker");

submit_button.addEventListener("click", function() {
    modal_one.classList.remove("show");
    modal_one.removeAttribute("role");
    modal_one.style = "display: none";

    modal_two.classList.add("show");
    modal_two.style = "display: inline-block; width: 150px";

    console.log("Test");
});


modal_two.classList.add("show");
modal_two.style = "display: inline-block; width: 150px";

console.log("Test");
});