const BASE_URL = "http://localhost:8080";
const token = localStorage.getItem("token");
const orderId = localStorage.getItem("latestOrderId");

let timeLeft = 30;

// ---------- TIMER ----------
const timer = setInterval(() => {
    timeLeft--;

    document.getElementById("timer").innerText = timeLeft;

    if (timeLeft <= 0) {
        clearInterval(timer);

        alert("Time up! Redirecting to orders...");
        window.location.href = "order-history.html";
    }

}, 1000);


// ---------- CANCEL ORDER ----------
function cancelOrder() {

    fetch(`${BASE_URL}/users/orders/cancel?orderId=${orderId}`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(res => res.json())
    .then(() => {

        alert("Order Cancelled ❌");

        clearInterval(timer);

        // redirect
        window.location.href = "order-history.html";
    })
    .catch(err => {
        console.error(err);
        alert("Cancel failed");
    });
}