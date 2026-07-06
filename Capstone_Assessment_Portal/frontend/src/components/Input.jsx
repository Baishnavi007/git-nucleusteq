/**
 * Reusable Input Component
 */

import { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import "./Input.css";

function Input({
    label,
    type = "text",
    name,
    value,
    placeholder,
    onChange,
    required = false,
    error = ""
}) {

    const [showPassword, setShowPassword] = useState(false);

    const inputType =
        type === "password"
            ? (showPassword ? "text" : "password")
            : type;

    return (
        <div className="input-group">

            <label className="input-label">
                {label}
            </label>

            <div className="input-wrapper">

                <input
                    className="input-field"
                    type={inputType}
                    name={name}
                    value={value}
                    placeholder={placeholder}
                    onChange={onChange}
                    required={required}
                />

                {
                    type === "password" && (
                        <button
                            type="button"
                            className="eye-button"
                            onClick={() =>
                                setShowPassword(!showPassword)
                            }
                        >
                            {
                                showPassword
                                    ? <FaEyeSlash />
                                    : <FaEye />
                            }
                        </button>
                    )
                }

            </div>

            {
                error && (
                    <p className="error-text">
                        {error}
                    </p>
                )
            }

        </div>
    );
}

export default Input;