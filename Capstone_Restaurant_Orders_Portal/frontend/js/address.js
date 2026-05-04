const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");

document.addEventListener("DOMContentLoaded", loadAddresses);

function loadAddresses() {
    fetch(`${BASE_URL}/users/address`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById("addressList");
        container.innerHTML = "";

        data.forEach(a => {
            const div = document.createElement("div");

            div.className = "bg-white p-3 mb-2 shadow rounded";

            div.innerHTML = `
                <p>${a.street}, ${a.city}</p>
                <button onclick="selectAddress(${a.id})"
                    class="bg-green-500 text-white px-3 py-1 mt-2 rounded">
                    Select
                </button>
            `;

            container.appendChild(div);
        });
    });
}

function selectAddress(id) {
    fetch(`${BASE_URL}/users/address/select?addressId=${id}`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        }
    }).then(() => alert("Address selected ✅"));
}

function addAddress() {
    fetch(`${BASE_URL}/users/address/add`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            street: document.getElementById("street").value,
            city: document.getElementById("city").value,
            state: document.getElementById("state").value,
            pincode: document.getElementById("pincode").value
        })
    }).then(() => {
        alert("Address added");
        loadAddresses();
    });
}

function placeOrder() {
    fetch(`${BASE_URL}/orders/place`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {

        // ✅ SAVE ORDER ID
        localStorage.setItem("latestOrderId", data.id);

        alert("Order placed 🎉");

        // ✅ REDIRECT TO SUCCESS PAGE
        window.location.href = "order-success.html";
    })
    .catch(err => {
        console.error(err);
        alert("Failed to place order");
    });
}