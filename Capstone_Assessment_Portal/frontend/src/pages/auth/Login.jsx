/**
 * Login Page
 */

import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import {
    FaBook,
    FaChartLine,
    FaClock,
    FaShieldAlt,
    FaClipboardCheck,
} from "react-icons/fa";

import Input from "../../components/common/Input";
import Button from "../../components/common/Button";

import {
    loginUser,
    getPublicKey,
} from "../../services/authService";

import { encryptPassword } from "../../utils/encryption";
import { validateLoginForm } from "../../utils/validation";
import { getErrorMessage } from "../../utils/errorHandler";
import "./Login.css";
import { toast } from "react-toastify";

function Login() {

    // ---------------- Navigation ----------------

    const navigate = useNavigate();

    // ---------------- State ----------------

    const [loginData, setLoginData] = useState({

        email_or_username: "",
        password: "",

    });

    const [loading, setLoading] = useState(false);
    /**
     * Stores validation errors
     */
    const [errors, setErrors] = useState({});

    /**
     * Stores RSA public key
     * received from backend.
     */
    const [publicKey, setPublicKey] = useState("");

    // ---------------- Effects ----------------

    useEffect(() => {

        /**
         * Fetch public key
         * when login page loads.
         */
        const fetchPublicKey = async () => {

            try {

                const response = await getPublicKey();

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

    // ---------------- Event Handlers ----------------

    const handleInputChange = (event) => {

        const { name, value } = event.target;

        setLoginData((previousData) => ({

            ...previousData,

            [name]: value,

        }));
        /***
         * Remove validation error when user starts typing
         */
        setErrors((previousErrors) =>({
            ...previousErrors,
            [name]: ""
        }))

    };

    const handleLogin = async (event) => {

        event.preventDefault();
        setErrors({});

        /**
         * Validate login form
         */
        const validationErrors =validateLoginForm(
            loginData
        );

        if(Object.keys(validationErrors).length>0){
            setErrors(validationErrors);
            return;
        }

        setLoading(true);

        try {

            if (!publicKey) {

                toast.error(
                    "Secure connection could not be established."
                );

                return;

            }

            /**
             * Encrypt password
             */

            const encryptedPassword = encryptPassword(

                loginData.password,

                publicKey

            );

            const payload = {

                ...loginData,

                password: encryptedPassword,

            };

            const response = await loginUser(
                payload
            );
            console.log(response);
            toast.success("Login Successful")

            /**
             * Store authentication data.
             */
            localStorage.setItem(
                "access_token",
                response.access_token
            );

            localStorage.setItem(
                "refresh_token",
                response.refresh_token
            );

            localStorage.setItem(
                "role",
                response.role
            );

            localStorage.setItem(
                "username",
                response.username
            );

            /**
             * Redirect user
             * based on role.
             */
            if (response.role === "admin") {

                navigate(
                    "/admin/dashboard"
                );

            }

            else {

                navigate(
                    "/student/dashboard"
                );

            }

        }

        catch (error) {

            toast.error(

                getErrorMessage(error)

            );

        }

        finally {

            setLoading(false);

        }

    };

    // ---------------- UI ----------------

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
                        noValidate
                    >

                        <Input
                            label="Username / Email"
                            type="text"
                            name="email_or_username"
                            value={loginData.email_or_username}
                            placeholder="Enter username or email"
                            onChange={handleInputChange}
                            error={errors.email_or_username}
                        />

                        <Input
                            label="Password"
                            type="password"
                            name="password"
                            value={loginData.password}
                            placeholder="Enter password"
                            onChange={handleInputChange}
                            error={errors.password}
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