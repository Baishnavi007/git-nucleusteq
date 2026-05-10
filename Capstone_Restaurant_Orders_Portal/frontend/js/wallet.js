const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");

document.addEventListener("DOMContentLoaded", loadBalance);

// ---------- LOAD BALANCE ----------
async function loadBalance() {
    try {
        const res = await fetch(`${BASE_URL}/users/profile`, {
            headers: { "Authorization": "Bearer " + token }
        });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(data.message || "Failed to load wallet");
        }
        document.getElementById("balance").innerText = "₹" + (data.walletBalance || 0);
    } catch (err) {
        console.error(err);
        alert(err.message || "Failed to load wallet");
    }
}

// ---------- ADD MONEY ----------
async function addMoney() {
    const amount = document.getElementById("amount").value;

    if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
        alert("Enter a valid positive amount");
        return;
    }

    try {
        const res = await fetch(`${BASE_URL}/users/wallet/add?amount=${amount}`, {
            method: "POST",
            headers: { "Authorization": "Bearer " + token }
        });

        const data = await res.json().catch(() => null);
        if (!res.ok) {
            const message = (data && data.message) ? data.message : "Failed to add money";
            throw new Error(message);
        }

        document.getElementById("balance").innerText = "₹" + data;
        document.getElementById("amount").value = "";
        alert("Money added successfully");
    } catch (err) {
        console.error(err);
        alert(err.message || "Failed to add money");
    }
}