/**
 * Reusable Button Component
 */

import "./Button.css";

function Button({
    text,
    type = "button",
    onClick,
    disabled = false,
    loading = false
}) {
    return (
        <button
            className="primary-button"
            type={type}
            onClick={onClick}
            disabled={disabled || loading}
        >
            {
                loading
                    ? "Please wait..."
                    : text
            }
        </button>
    );
}

export default Button;