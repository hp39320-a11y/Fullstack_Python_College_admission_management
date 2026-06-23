document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("addressModal");
    const openBtn = document.getElementById("changeAddressBtn");
    const closeBtn = document.getElementById("closeModal");
    const radios = document.querySelectorAll('input[name="address"]');
    const selectedText = document.getElementById("selectedAddress");
    const addNewBtn = document.getElementById("addNewBtn");
    const newForm = document.getElementById("newAddressForm");

    // OPEN MODAL
    openBtn.addEventListener("click", () => {
        modal.classList.add("active");
    });

    // CLOSE MODAL
    closeBtn.addEventListener("click", () => {
        modal.classList.remove("active");
    });

    // CLICK OUTSIDE CLOSE
    window.addEventListener("click", (e) => {
        if (e.target === modal) {
            modal.classList.remove("active");
        }
    });

    // 🔥 SELECT ADDRESS (MAIN FIX)
    radios.forEach(radio => {
        radio.addEventListener("change", function () {

            if (this.value !== "new") {

                const card = this.closest(".modal-card");

                const name = card.querySelector(".name").innerText;
                const lines = card.querySelectorAll("p");

                const address = lines[1].innerText;
                const city = lines[2].innerText;
                const phone = lines[3].innerText;

                // ✅ UPDATE UI PROPERLY
                selectedText.innerText = `${name}, ${address}, ${city}, ${phone}`;

                // CLOSE MODAL
                modal.classList.remove("active");
            }
        });
    });

    // ADD NEW FORM
    addNewBtn.addEventListener("click", () => {
        newForm.style.display = "block";
    });

});