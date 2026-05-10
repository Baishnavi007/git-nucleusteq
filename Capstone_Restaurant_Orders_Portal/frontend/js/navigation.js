function selectRole(role) {
    localStorage.setItem("role", role);
    window.location.href = "auth.html";
}