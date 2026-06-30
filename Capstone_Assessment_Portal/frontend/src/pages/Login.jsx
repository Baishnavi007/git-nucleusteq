/**
 * Login Page
 */

import { useState, useEffect } from "react";
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

import { loginUser,getPublicKey } from "../services/authService";

import { encryptPassword } from "../utils/encryption";
import "./Login.css";

function Login() {

    const navigate = useNavigate();

    const [loginData, setLoginData] = useState({
        email_or_username: "",
        password: ""
    });

    const [loading, setLoading] = useState(false);

    /**
      * Stores RSA public key received from backend.
    */
    const [publicKey, setPublicKey] = useState("");
    /**
 * Fetch public key
 * when login page loads.
 */
useEffect(() => {

    const fetchPublicKey = async () => {

        try {

            const response = await getPublicKey();

            console.log("Response:", response);
        console.log("Public Key:", response.publicKey);
        console.log("Length:", response.publicKey.length);
            setPublicKey(
                response.publicKey
            );

        }

        catch (error) {

            console.error(
                "Unable to fetch public key.",
                error
            );

        }

    };

    fetchPublicKey();

}, []);

    const handleInputChange = (event) => {

        const { name, value } = event.target;

        setLoginData((previousData) => ({
            ...previousData,
            [name]: value
        }));
    };


    const handleLogin = async (event) => {

        event.preventDefault();

        setLoading(true);

        try {

    if (!publicKey) {

        alert(
            "Secure connection could not be established."
        );

        return;

    }

    const encryptedPassword = encryptPassword(

        loginData.password,

        publicKey

    );

    console.log("Encrypted Password:", encryptedPassword);
console.log("Encrypted Length:", encryptedPassword.length);
    const payload = {

        ...loginData,

        password: encryptedPassword

    };

    const response = await loginUser(
        payload
    );

            // Save JWT Token
            localStorage.setItem(
                "access_token",
                response.access_token
            );

            // Save Refresh Token
             localStorage.setItem(

              "refresh_token",

               response.refresh_token

                );
            // Save Role
            localStorage.setItem(
                "role",
                response.role
            );

            // Redirect according to role

            if (response.role === "admin") {

                navigate("/admin/dashboard");

            } else {

                navigate("/student/dashboard");

            }

        }

        catch (error) {

            alert(

                error.response?.data?.detail ||

                "Login Failed"

            );

        }

        finally {

            setLoading(false);

        }

    };


    return (

        <div className="login-page">

            {/* LEFT PANEL */}

            <section className="login-left">

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

                        Practice Smarter.
                        <br />
                        Analyze Better.
                        <br />
                        Improve Everyday.

                    </h2>

                    <p className="description">

                        Prepare yourself through topic-wise quizzes,
                        timed assessments and instant analytics.

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

            <section className="login-right">

                <div className="login-card">

                    <h2>

                        Welcome Back 👋

                    </h2>

                    <p>

                        Login to continue your assessment journey.

                    </p>

                    <form
                        onSubmit={handleLogin}
                    >

                        <Input
                            label="Username / Email"
                            type="text"
                            name="email_or_username"
                            value={loginData.email_or_username}
                            placeholder="Enter username or email"
                            onChange={handleInputChange}
                            required
                        />

                        <Input
                            label="Password"
                            type="password"
                            name="password"
                            value={loginData.password}
                            placeholder="Enter password"
                            onChange={handleInputChange}
                            required
                        />

                        <Button
                            text="Login"
                            type="submit"
                            loading={loading}
                        />

                    </form>

                    <div className="divider">

                        <span>

                            OR

                        </span>

                    </div>

                    <div className="register-section">

                        <p>

                            New to Assessment Portal?

                        </p>

                        <Link
                            to="/register"
                            className="register-link"
                        >

                            Create Account

                        </Link>

                    </div>

                </div>

            </section>

        </div>

    );

}

export default Login;
