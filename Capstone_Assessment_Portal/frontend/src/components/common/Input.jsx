/**
 * Reusable Input Component
 */

import { useState } from "react";
import {
    FaEye,
    FaEyeSlash
} from "react-icons/fa";

import "./Input.css";

function Input({

    label,

    type = "text",

    name,

    value,

    placeholder,

    onChange,

    error = ""

}) {

    /**
     * Controls password visibility.
     */
    const [showPassword, setShowPassword] = useState(false);

    /**
     * Determines the input type.
     */
    const inputType =

        type === "password"

            ? (

                showPassword

                    ? "text"

                    : "password"

            )

            : type;

    return (

        <div className="input-group">

            <label className="input-label">

                {label}

            </label>

            <div className="input-wrapper">

                <input

                    className={
                        error
                            ? "input-field input-error"
                            : "input-field"
                    }

                    type={inputType}

                    name={name}

                    value={value}

                    placeholder={placeholder}

                    onChange={onChange}

                />

                {

                    type === "password" && (

                        <button

                            type="button"

                            className="eye-button"

                            onClick={() =>

                                setShowPassword(

                                    !showPassword

                                )

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

                    <small className="error-text">

                        {error}

                    </small>

                )

            }

        </div>

    );

}

export default Input;