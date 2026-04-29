const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");

document.addEventListener("DOMContentLoaded", loadBalance);

// ---------- LOAD BALANCE ----------
function loadBalance() {
    fetch(`${BASE_URL}/users/profile`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("balance").innerText = "₹" + (data.walletBalance || 0);
    })
    .catch(err => console.error(err));
}

// ---------- ADD MONEY ----------
function addMoney() {

    console.log("BUTTON CLICKED");

    const amount = document.getElementById("amount").value;
    console.log("Amount:", amount);

    if (!amount) {
        alert("Enter amount first!");
        return;
    }

    fetch(`${BASE_URL}/users/wallet/add?amount=${amount}`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => {
        console.log("Response status:", res.status);

        if (!res.ok) {
            throw new Error("Failed to add money");
        }
        return res.json();
    })
    .then(data => {
        console.log("Updated Balance:", data);

        document.getElementById("balance").innerText = "₹" + data;

        alert("Money added successfully 💰");
    })
    .catch(err => {
        console.error(err);
        alert("Failed to add money");
    });
}