document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("addressModal");
    const openBtn = document.getElementById("changeAddressBtn");
    const closeBtn = document.getElementById("closeModal");

    const radios = document.querySelectorAll('input[name="address"]');
    const selectedText = document.getElementById("selectedAddress");

    const addNewBtn = document.getElementById("addNewBtn");
    const newForm = document.getElementById("newAddressForm");

    // Modal open/close
    openBtn.onclick = () => modal.classList.add("active");
    closeBtn.onclick = () => modal.classList.remove("active");

    window.onclick = (e) => {
        if (e.target === modal) modal.classList.remove("active");
    };

    // Update address UI only
    function updateAddress(card) {
        const name = card.querySelector(".name").innerText;
        const addr = card.querySelector(".addr").innerText;
        const city = card.querySelector(".city").innerText;

        selectedText.innerText = `${name}, ${addr}, ${city}`;
    }

    radios.forEach(radio => {
        radio.onchange = function () {
            updateAddress(this.closest(".modal-card"));
            modal.classList.remove("active");
        }
    });

    const first = document.querySelector('input[name="address"]:checked');
    if (first) updateAddress(first.closest(".modal-card"));

    // Show new address form
    addNewBtn.onclick = () => newForm.style.display = "block";

});