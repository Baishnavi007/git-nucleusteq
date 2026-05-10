const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");

document.addEventListener("DOMContentLoaded", loadAddresses);

async function loadAddresses() {
    try {
        const res = await fetch(`${BASE_URL}/users/address`, {
            headers: { "Authorization": "Bearer " + token }
        });
        const data = await res.json().catch(() => []);
        if (!res.ok) {
            throw new Error(data.message || "Failed to load addresses");
        }

        const container = document.getElementById("addressList");
        container.innerHTML = "";

        if (!Array.isArray(data) || data.length === 0) {
            container.innerHTML = `<p class="text-gray-400">No saved addresses yet.</p>`;
            return;
        }

        data.forEach(a => {

    const div = document.createElement("div");

    div.className =
        "address-card bg-white p-3 mb-2 shadow rounded border-2 border-transparent";

    div.innerHTML = `
        <p>${escapeHtml(a.street)}, ${escapeHtml(a.city)}</p>

        <button
            class="bg-green-500 text-white px-3 py-1 mt-2 rounded">
            Select
        </button>
    `;

    const button = div.querySelector("button");

    button.addEventListener("click", async function () {

        try {

            const res = await fetch(
                `${BASE_URL}/users/address/select?addressId=${a.id}`,
                {
                    method: "POST",
                    headers: {
                        "Authorization": "Bearer " + token
                    }
                }
            );

            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                throw new Error(data.message || "Failed to select address");
            }

            // sab cards normal
            document.querySelectorAll(".address-card").forEach(card => {
                card.classList.remove(
                    "bg-green-200",
                    "border-green-600"
                );
            });

            // selected green
            div.classList.add(
                "bg-green-200",
                "border-green-600"
            );

        } catch (err) {
            console.error(err);
            alert(err.message || "Failed to select address");
        }

    });

    container.appendChild(div);
});
    } catch (err) {
        console.error(err);
        alert(err.message || "Failed to load addresses");
    }
}

async function selectAddress(id) {
    try {
        const res = await fetch(`${BASE_URL}/users/address/select?addressId=${id}`, {
            method: "POST",
            headers: { "Authorization": "Bearer " + token }
        });
        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data.message || "Failed to select address");
        }
        alert("Address selected");
    } catch (err) {
        console.error(err);
        alert(err.message || "Failed to select address");
    }
}

async function addAddress() {
    const street = document.getElementById("street").value.trim();
    const city = document.getElementById("city").value.trim();
    const state = document.getElementById("state").value.trim();
    const pincode = document.getElementById("pincode").value.trim();

    if (!street || !city || !state || !pincode) {
        alert("All fields are required");
        return;
    }

    try {
        const res = await fetch(`${BASE_URL}/users/address/add`, {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ street, city, state, pincode })
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(data.message || "Failed to add address");
        }
        alert("Address added");
        document.getElementById("street").value = "";
        document.getElementById("city").value = "";
        document.getElementById("state").value = "";
        document.getElementById("pincode").value = "";
        loadAddresses();
    } catch (err) {
        console.error(err);
        alert(err.message || "Failed to add address");
    }
}

async function placeOrder() {
    try {
        const res = await fetch(`${BASE_URL}/orders/place`, {
            method: "POST",
            headers: { "Authorization": "Bearer " + token }
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(data.message || "Failed to place order");
        }

        localStorage.setItem("latestOrderId", data.id);
        alert("Order placed");
        window.location.href = "order-success.html";
    } catch (err) {
        console.error(err);
        alert(err.message || "Failed to place order");
    }
}

function escapeHtml(text) {
    if (text == null) return "";
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}