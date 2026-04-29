const BASE_URL = "http://localhost:8080";

let isLogin = true;

document.addEventListener("DOMContentLoaded", () => {

    const toggleText = document.getElementById("toggleText");
    const formTitle = document.getElementById("formTitle");
    const submitBtn = document.getElementById("submitBtn");

    const firstNameInput = document.getElementById("firstName");
    const lastNameInput = document.getElementById("lastName");
    const phoneInput = document.getElementById("phone");

    toggleText.addEventListener("click", () => {

        isLogin = !isLogin;

        if (isLogin) {
            formTitle.innerText = "Login";
            submitBtn.innerText = "Login";
            toggleText.innerText = "New user? Register here";

            firstNameInput.classList.add("hidden");
            lastNameInput.classList.add("hidden");
            phoneInput.classList.add("hidden");

        } else {
            formTitle.innerText = "Register";
            submitBtn.innerText = "Register";
            toggleText.innerText = "Already have an account? Login";

            firstNameInput.classList.remove("hidden");
            lastNameInput.classList.remove("hidden");
            phoneInput.classList.remove("hidden");
        }

        clearError();
    });

    submitBtn.addEventListener("click", handleAuth);
});


// ================= ERROR HANDLING =================

function showError(msg) {
    const error = document.getElementById("errorMsg");
    error.innerText = msg;
    error.classList.remove("hidden");
}

function clearError() {
    const error = document.getElementById("errorMsg");
    error.classList.add("hidden");
}


// ================= VALIDATION =================

function validateForm() {

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
        showError("Email and Password are mandatory");
        return false;
    }

    if (!isLogin) {

        const firstName = document.getElementById("firstName").value.trim();
        const lastName = document.getElementById("lastName").value.trim();
        const phone = document.getElementById("phone").value.trim();

        if (!firstName) {
            showError("First Name is mandatory");
            return false;
        }

        if (!lastName) {
            showError("Last Name is mandatory");
            return false;
        }

        if (!phone) {
            showError("Phone number is mandatory");
            return false;
        }
    }

    clearError();
    return true;
}


// ================= MAIN AUTH FUNCTION =================

async function handleAuth() {

    if (!validateForm()) return;

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const role = localStorage.getItem("role");

    let url = "";
    let body = {};

    try {

        if (isLogin) {

            url = `${BASE_URL}/auth/login`;

            body = {
                email: email,
                password: password
            };

        } else {

            url = `${BASE_URL}/auth/register`;

            body = {
                firstName: document.getElementById("firstName").value.trim(),
                lastName: document.getElementById("lastName").value.trim(),
                phoneNumber: document.getElementById("phone").value.trim(),
                email: email,
                password: password,
                role: role
            };
        }

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        console.log("Response:", data);

        if (!response.ok) {
            showError(data.message || "Something went wrong");
            return;
        }

        // ================= LOGIN FLOW =================
        if (isLogin) {

            if (!data.token) {
                showError("Invalid credentials");
                return;
            }

            // 🔴 ROLE VALIDATION (MAIN FIX)
            if (data.role !== role) {
                showError("Invalid user type selected");
                return;  // 🚨 STOP HERE (VERY IMPORTANT)
            }

            // ✅ store only AFTER validation
            localStorage.setItem("token", data.token);

            if (role === "RESTAURANT_OWNER") {
                window.location.href = "owner.html";
            } else {
                window.location.href = "user.html";
            }

        } 
        // ================= REGISTER FLOW =================
        else {

            alert("Registration successful. Please login.");
            window.location.href = "auth.html";
        }

    } catch (err) {
        console.error(err);
        showError("Server error. Try again.");
    }
}