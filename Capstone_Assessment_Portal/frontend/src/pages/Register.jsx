/**
 * Register Page
 */

import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import {
    FaBook,
    FaChartLine,
    FaClock,
    FaShieldAlt,
    FaClipboardCheck
} from "react-icons/fa";

import Input from "../components/Input";
import Button from "../components/Button";

import { registerUser } from "../services/authService";

import "./Register.css";

function Register() {

    const navigate = useNavigate();

    const [registerData, setRegisterData] = useState({

        first_name: "",
        last_name: "",
        username: "",
        email: "",
        password: "",
        confirm_password: ""

    });

    const [loading, setLoading] = useState(false);

    const handleInputChange = (event) => {

        const { name, value } = event.target;

        setRegisterData((previousData) => ({

            ...previousData,

            [name]: value

        }));

    };

    const handleRegister = async (event) => {

        event.preventDefault();

        if (
            registerData.password !==
            registerData.confirm_password
        ) {

            alert("Passwords do not match.");

            return;

        }

        try {

            setLoading(true);

            const payload = {

                first_name: registerData.first_name,
                last_name: registerData.last_name,
                username: registerData.username,
                email: registerData.email,
                password: registerData.password

            };

            const response = await registerUser(payload);

            alert(response.message);

            navigate("/");

        }

        catch (error) {

            alert(

                error.response?.data?.detail ||

                "Registration Failed"

            );

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div className="register-page">

            {/* LEFT PANEL */}

            <section className="register-left">

                <div className="overlay"></div>

                <div className="left-content">

                    <div className="logo-box">

                        <div className="logo-circle">

                            AP

                        </div>

                        <div>

                            <h1>

                                Assessment Portal

                            </h1>

                            <p>

                                Smart Online Assessment Platform

                            </p>

                        </div>

                    </div>

                    <h2>

                        Start Your Journey.
                        <br />
                        Learn.
                        <br />
                        Improve.

                    </h2>

                    <p className="description">

                        Join thousands of students preparing smarter with our
                        assessment platform.

                    </p>

                    <div className="feature-list">

                        <div className="feature-item">

                            <FaBook />

                            <span>

                                Topic-wise Assessments

                            </span>

                        </div>

                        <div className="feature-item">

                            <FaClock />

                            <span>

                                Timed Practice Tests

                            </span>

                        </div>

                        <div className="feature-item">

                            <FaChartLine />

                            <span>

                                Performance Analytics

                            </span>

                        </div>

                        <div className="feature-item">

                            <FaClipboardCheck />

                            <span>

                                Instant Result Analysis

                            </span>

                        </div>

                        <div className="feature-item">

                            <FaShieldAlt />

                            <span>

                                Secure Authentication

                            </span>

                        </div>

                    </div>

                </div>

            </section>

            {/* RIGHT PANEL */}

            <section className="register-right">

                <div className="register-card">

                    <h2>

                        Create Account ✨

                    </h2>

                    <p>

                        Register to begin your assessment journey.

                    </p>

                    <form
                        onSubmit={handleRegister}
                    >

                        <div className="row">

                            <Input
                                label="First Name"
                                name="first_name"
                                value={registerData.first_name}
                                placeholder="Enter first name"
                                onChange={handleInputChange}
                                required
                            />

                            <Input
                                label="Last Name"
                                name="last_name"
                                value={registerData.last_name}
                                placeholder="Enter last name"
                                onChange={handleInputChange}
                                required
                            />

                        </div>

                        <Input
                            label="Username"
                            name="username"
                            value={registerData.username}
                            placeholder="Enter username"
                            onChange={handleInputChange}
                            required
                        />

                        <Input
                            label="Email"
                            type="email"
                            name="email"
                            value={registerData.email}
                            placeholder="Enter email"
                            onChange={handleInputChange}
                            required
                        />

                        <Input
                            label="Password"
                            type="password"
                            name="password"
                            value={registerData.password}
                            placeholder="Enter password"
                            onChange={handleInputChange}
                            required
                        />

                        <Input
                            label="Confirm Password"
                            type="password"
                            name="confirm_password"
                            value={registerData.confirm_password}
                            placeholder="Confirm password"
                            onChange={handleInputChange}
                            required
                        />

                        <Button
                            text="Create Account"
                            type="submit"
                            loading={loading}
                        />

                    </form>

                    <div className="divider">

                        <span>

                            OR

                        </span>

                    </div>

                    <div className="login-section">

                        <p>

                            Already have an account?

                        </p>

                        <Link
                            to="/"
                            className="login-link"
                        >

                            Login

                        </Link>

                    </div>

                </div>

            </section>

        </div>

    );

}

export default Register;