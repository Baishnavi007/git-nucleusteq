const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");

document.addEventListener("DOMContentLoaded", loadCart);

function loadCart() {
    fetch(`${BASE_URL}/cart`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById("cartItems");
        const total = document.getElementById("totalAmount");

        container.innerHTML = "";
        total.innerText = data.totalAmount || 0;

        if (!data.items || data.items.length === 0) {
            container.innerHTML = "<p>Your cart is empty 🥲</p>";
            return;
        }

        data.items.forEach(item => {
            const div = document.createElement("div");

            div.innerHTML = `
                <h4>${item.itemName}</h4>
                <p>₹${item.price} x ${item.quantity}</p>

                <button onclick="decrease(${item.menuItemId})">➖</button>
                <button onclick="removeItem(${item.menuItemId})">❌ Remove</button>
            `;

            container.appendChild(div);
        });
    });
}

// decrease
function decrease(menuItemId) {
    fetch(`${BASE_URL}/cart/decrease?menuItemId=${menuItemId}`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        }
    }).then(loadCart);
}

// remove
function removeItem(menuItemId) {
    fetch(`${BASE_URL}/cart/remove?menuItemId=${menuItemId}`, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + token
        }
    }).then(loadCart);
}

// navigation
function goBack() {
    window.location.href = "menu.html";
}

function goToCheckout() {
    window.location.href = "checkout.html";
}