// ==============================
// 🔐 CSRF TOKEN
// ==============================
function getCSRFToken() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}


// ==============================
// 🔔 TOAST MESSAGE
// ==============================
function showToast(message, type="success") {
    const toast = document.getElementById("toast");

    if (!toast) return;

    toast.innerText = message;
    toast.className = "show " + type;

    setTimeout(() => {
        toast.className = toast.className.replace("show", "");
    }, 2500);
}


// ==============================
// 🧠 GLOBAL CLICK HANDLER
// ==============================
document.addEventListener("click", function(e){

    // ==========================
    // 🛒 ADD TO CART
    // ==========================
    if(e.target.classList.contains("add-to-cart-btn")){

        const productId = e.target.dataset.id;

        fetch(`/cart/add/${productId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            }
        })
        .then(res => {
            if (res.ok) {
                showToast("Item added to cart 🛒");
            } else {
                showToast("Error adding to cart", "error");
            }
        });
    }


    // ==========================
    // ❤️ WISHLIST (BUTTON + ICON)
    // ==========================
    const wishBtn = e.target.closest(".wishlist-btn, .wishlist-icon");

    if(wishBtn){

        const productId = wishBtn.dataset.id;

        fetch(`/wishlist/add/${productId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
            }
        })
        .then(res => {
            if (res.ok) {
                showToast("Added to wishlist ❤️");
            } else {
                showToast("Error adding to wishlist", "error");
            }
        });
    }


    // ==========================
    // ❌ OPEN CANCEL MODAL (FIXED)
    // ==========================
    const cancelBtn = e.target.closest(".open-cancel-modal");

    if(cancelBtn){

        e.preventDefault();

        const url = cancelBtn.getAttribute("data-url");

        const modal = document.getElementById("cancelModal");
        modal.classList.add("show");

        document.getElementById("confirmCancelBtn").href = url;
    }


    // ==========================
    // ❌ CLOSE MODAL BUTTON
    // ==========================
    if(e.target.classList.contains("close-modal")){
        closeModal();
    }

});


// ==============================
// ❌ CLOSE MODAL FUNCTION
// ==============================
function closeModal(){
    const modal = document.getElementById("cancelModal");
    if(modal){
        modal.classList.remove("show");
    }
}


// ==============================
// ❌ CLOSE ON OUTSIDE CLICK
// ==============================
window.addEventListener("click", function(e){
    const modal = document.getElementById("cancelModal");

    if(e.target === modal){
        modal.classList.remove("show");
    }
});


// ==============================
// 📏 SIZE SELECT
// ==============================
function selectSize(btn){

    document.querySelectorAll(".size-btn").forEach(b => {
        b.classList.remove("active");
    });

    btn.classList.add("active");

    const input = document.getElementById("selected-size");
    if(input){
        input.value = btn.dataset.size;
    }
}


// ==============================
// 🎉 CANCEL SUCCESS POPUP
// ==============================
window.addEventListener("load", function(){

    const successBox = document.getElementById("cancelSuccess");

    if(successBox){
        successBox.style.display = "flex";

        setTimeout(() => {
            successBox.style.display = "none";
        }, 2500);
    }

});