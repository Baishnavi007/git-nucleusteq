const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");

if (!token) {
    alert("Session expired. Please login again.");
    window.location.href = "auth.html";
}

document.addEventListener("DOMContentLoaded", () => {
    loadMenu();
    loadCart();
});

// ---------- LOAD MENU ----------
function loadMenu() {

    const restaurantId = localStorage.getItem("restaurantId");

    fetch(`${BASE_URL}/users/restaurants/${restaurantId}/menu`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {

        const container = document.getElementById("menuContainer");
        container.innerHTML = "";

        data.forEach(category => {

            const items = category.items || [];

            const div = document.createElement("div");
            div.className = "bg-white rounded-2xl shadow-lg p-6 mb-6";

            div.innerHTML = `
                <h2 class="text-xl font-bold mb-4 text-gray-800">
                    ${category.categoryName}
                </h2>

                <div class="space-y-3">
                    ${items.map(item => `
                        <div class="flex justify-between items-center border p-4 rounded-xl hover:shadow transition">

                            <div>
                                <p class="font-semibold text-gray-800">
                                    ${item.name}
                                </p>
                                <p class="text-sm text-gray-500">
                                    ${item.description || "No description"}
                                </p>
                            </div>

                            <div class="text-right">
                                <p class="text-green-600 font-bold mb-2">
                                    ₹${item.price}
                                </p>

                                <button onclick="addToCart(${item.id})"
                                    class="bg-green-500 text-white px-3 py-1 rounded-lg hover:bg-green-600">
                                    Add
                                </button>
                            </div>

                        </div>
                    `).join("")}
                </div>
            `;

            container.appendChild(div);
        });
    });
}

// ---------- ADD TO CART ----------
function addToCart(itemId) {

    fetch(`${BASE_URL}/cart/add?menuItemId=${itemId}&quantity=1`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(async res => {
        const data = await res.json();

        if (!res.ok) {
            
            throw new Error(data.message || "Something went wrong");
        }

        return data;
    })
    .then(() => {
        loadCart(); 
    })
    .catch(err => {
        showToast(err.message); 
    });
}

// ----Showing error message---
function showToast(message) {
    const toast = document.getElementById("toast");

    toast.innerText = message;
    toast.classList.remove("hidden");

    setTimeout(() => {
        toast.classList.add("hidden");
    }, 3000);
}
// ---------- LOAD CART ----------
function loadCart() {
    fetch(`${BASE_URL}/cart`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {

        const cartContainer = document.getElementById("cartItems");
        const total = document.getElementById("cartTotal");

        cartContainer.innerHTML = "";

        if (!data.items || data.items.length === 0) {
            cartContainer.innerHTML = `<p class="text-gray-400">Cart is empty 🛒</p>`;
            total.innerText = "0";
            return;
        }

        data.items.forEach(item => {
            cartContainer.innerHTML += `
                <div class="flex justify-between items-center mb-3">

                    <div>
                        <p class="font-medium">${item.itemName}</p>
                        <p class="text-sm text-gray-500">₹${item.price}</p>
                    </div>

                    <div class="flex items-center gap-2">
                        <button onclick="decreaseItem('${item.itemName}')"
                            class="bg-gray-200 px-2 rounded">-</button>

                        <span>${item.quantity}</span>

                        <button onclick="addToCartByName('${item.itemName}')"
                            class="bg-gray-200 px-2 rounded">+</button>
                    </div>
                </div>
            `;
        });

        total.innerText = data.totalAmount;
    });
}

// ---------- DECREASE ----------
function decreaseItem(itemName) {
    fetch(`${BASE_URL}/cart/decrease?menuItemId=${getId(itemName)}`, {
        method: "POST",
        headers: { "Authorization": "Bearer " + token }
    }).then(() => loadCart());
}

// ---------- CLEAR ----------
function clearCart() {
    fetch(`${BASE_URL}/cart/clear`, {
        method: "DELETE",
        headers: { "Authorization": "Bearer " + token }
    }).then(() => loadCart());
}

// helper (simple)
function getId(name) {
    return 1;
}