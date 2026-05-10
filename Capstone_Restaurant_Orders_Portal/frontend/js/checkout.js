const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");

document.addEventListener("DOMContentLoaded", loadCart);

// ================= LOAD CART =================
function loadCart() {
    fetch(`${BASE_URL}/cart`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {

        const container = document.getElementById("orderItems");
        const total = document.getElementById("totalAmount");

        container.innerHTML = "";
        total.innerText = data.totalAmount || 0;

        if (!data.items || data.items.length === 0) {
            container.innerHTML = "<p>Your cart is empty 🥲</p>";
            return;
        }

        data.items.forEach(item => {
            const div = document.createElement("div");

            div.className = "border-b py-2";

            div.innerHTML = `
                <p>${item.itemName}</p>
                <p>₹${item.price} x ${item.quantity}</p>
            `;

            container.appendChild(div);
        });
    })
    .catch(err => {
        console.error(err);
        alert("Failed to load cart");
    });
}


// ================= PLACE ORDER =================
async function placeOrder() {
    try {
        const res = await fetch(`${BASE_URL}/orders/place`, {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        const data = await res.json();

        if (!res.ok) {
            alert(data.message || "Order failed");
            return;
        }

        // SAVE ORDER ID
        localStorage.setItem("latestOrderId", data.id);

        // redirect to success page
        window.location.href = "order-success.html";

    } catch (err) {
        console.error(err);
        alert("Something went wrong while placing order");
    }
}


// ================= NAVIGATION =================
function goToAddress() {
    window.location.href = "address.html";
}