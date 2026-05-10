const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");
const orderId = localStorage.getItem("latestOrderId");

let timeLeft = 30;

// ---------- TIMER ----------
const timer = setInterval(() => {
    timeLeft--;

    const timerEl = document.getElementById("timer");
    if (timerEl) timerEl.innerText = timeLeft;

    if (timeLeft <= 0) {
        clearInterval(timer);

        alert("Time up! Redirecting to Home...");
        window.location.href = "user.html";
    }
}, 1000);


// ---------- CANCEL ORDER ----------
async function cancelOrder() {

    if (!orderId) {
        alert("No order to cancel");
        return;
    }

    try {
        const res = await fetch(`${BASE_URL}/users/orders/cancel?orderId=${orderId}`, {
            method: "POST",
            headers: { "Authorization": "Bearer " + token }
        });

        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
            throw new Error(data.message || "Cancel failed");
        }

        alert("Order Cancelled");
        clearInterval(timer);
        window.location.href = "order-history.html";
    } catch (err) {
        console.error(err);
        alert(err.message || "Cancel failed");
    }
}