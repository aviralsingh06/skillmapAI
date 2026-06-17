import sys
import os

# Add project root to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st

from firebase_config import is_firebase_configured
from services.firebase_service import (
    send_password_reset,
    sign_in,
    sign_up,
)


def init_auth_session():
    """
    Initialise all auth-related session-state keys with safe defaults.
    Must be called at the very top of every page, before any st.* calls.
    Uses setdefault so existing values (from a prior run or mobile reload)
    are never overwritten.
    """
    defaults = {
        "authenticated": False,
        "user_uid": None,
        "user_email": None,
        "user_name": None,
        "user_created_at": None,
        "id_token": None,
        "refresh_token": None,
    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def _persist_session(user):
    """Write all fields from a successful auth response into session state."""
    st.session_state.authenticated = True
    st.session_state.user_uid = user["uid"]
    st.session_state.user_email = user["email"]
    st.session_state.user_name = user.get(
        "display_name",
        user["email"]
    )
    st.session_state.user_created_at = user.get("created_at")
    st.session_state.id_token = user["id_token"]
    st.session_state.refresh_token = user["refresh_token"]


def _clear_session():
    """Reset all auth-related session keys to their safe defaults."""
    st.session_state.authenticated = False
    st.session_state.user_uid = None
    st.session_state.user_email = None
    st.session_state.user_name = None
    st.session_state.user_created_at = None
    st.session_state.id_token = None
    st.session_state.refresh_token = None


def logout_user():
    """Clear session and rerun so the login page appears."""
    _clear_session()
    st.rerun()


def _inject_auth_css():
    st.markdown(
        """
        <style>
        .auth-wrapper {
            max-width: 460px;
            margin: 2rem auto 3rem;
            padding: 2rem 2.2rem;
            border: 1px solid rgba(124, 58, 237, 0.34);
            border-radius: 22px;
            background: linear-gradient(
                135deg,
                rgba(124, 58, 237, 0.14),
                rgba(17, 24, 39, 0.92)
            );
            box-shadow: 0 20px 55px rgba(0, 0, 0, 0.28);
        }
        .auth-brand {
            color: #67e8f9;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }
        .auth-title {
            color: #f8fafc;
            font-size: 1.85rem;
            font-weight: 800;
            margin: 0 0 0.35rem;
        }
        .auth-subtitle {
            color: #94a3b8;
            font-size: 0.92rem;
            line-height: 1.55;
            margin-bottom: 1.4rem;
        }
        .auth-footer {
            color: #64748b;
            font-size: 0.82rem;
            text-align: center;
            margin-top: 1.2rem;
        }
        div[data-testid="stForm"] {
            border: 1px solid rgba(148, 163, 184, 0.14);
            border-radius: 16px;
            padding: 1.2rem 1.3rem 1.4rem;
            background: rgba(15, 23, 42, 0.72);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_auth_page():
    """
    Render the login / sign-up / forgot-password page.

    Mobile session fix: returns immediately (without rendering anything)
    when the user is already authenticated. This prevents the login form
    from flashing on screen during Streamlit's rerun cycle on mobile,
    which previously caused the session to appear lost.
    """

    # ── FIX: Early return when already authenticated.
    # On mobile, Streamlit reruns the entire script on every interaction.
    # Without this guard the auth form rendered briefly each time, which
    # made it look like the user was logged out after uploading a file.
    if st.session_state.get("authenticated", False):
        return

    if not is_firebase_configured():
        st.error(
            "Firebase is not configured. "
            "Please check your environment variables or Streamlit secrets."
        )
        return

    _inject_auth_css()

    st.markdown(
        """
        <div class="auth-wrapper">
            <div class="auth-brand">
                SkillMap AI
            </div>
            <div class="auth-title">
                Welcome back
            </div>
            <div class="auth-subtitle">
                Sign in to access your
                resume intelligence dashboard,
                saved analyses,
                and progress analytics.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_login, tab_signup, tab_reset = st.tabs(
        ["Login", "Sign Up", "Forgot Password"]
    )

    with tab_login:
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "Email",
                placeholder="you@example.com"
            )
            password = st.text_input(
                "Password",
                type="password"
            )
            submitted = st.form_submit_button(
                "Sign In",
                use_container_width=True,
                type="primary"
            )

            if submitted:
                if not email or not password:
                    st.warning(
                        "Please enter both email and password."
                    )
                else:
                    with st.spinner("Signing in…"):
                        user, error = sign_in(
                            email.strip(),
                            password
                        )

                    if error:
                        st.error(error)
                    else:
                        _persist_session(user)
                        st.success("Logged in successfully!")
                        st.rerun()

    with tab_signup:
        with st.form("signup_form", clear_on_submit=False):
            name = st.text_input(
                "Full Name",
                placeholder="Your name"
            )
            email = st.text_input(
                "Email",
                placeholder="you@example.com",
                key="signup_email"
            )
            password = st.text_input(
                "Password",
                type="password"
            )
            confirm = st.text_input(
                "Confirm Password",
                type="password"
            )
            submitted = st.form_submit_button(
                "Create Account",
                use_container_width=True,
                type="primary"
            )

            if submitted:
                if not email or not password:
                    st.warning("Email and password are required.")

                elif password != confirm:
                    st.warning("Passwords do not match.")

                elif len(password) < 6:
                    st.warning(
                        "Password must be at least 6 characters."
                    )

                else:
                    with st.spinner("Creating account…"):
                        user, error = sign_up(
                            email.strip(),
                            password,
                            name.strip() if name else None
                        )

                    if error:
                        st.error(error)
                    else:
                        _persist_session(user)
                        st.success("Account created!")
                        st.rerun()

    with tab_reset:
        with st.form("reset_form", clear_on_submit=False):
            email = st.text_input(
                "Email",
                placeholder="you@example.com",
                key="reset_email"
            )
            submitted = st.form_submit_button(
                "Send Reset Link",
                use_container_width=True
            )

            if submitted:
                if not email:
                    st.warning("Please enter your email address.")
                else:
                    with st.spinner("Sending reset email…"):
                        success, message = send_password_reset(
                            email.strip()
                        )

                    if success:
                        st.success(
                            f"Password reset email sent to {message}."
                        )
                    else:
                        st.error(message)

    st.markdown(
        '<div class="auth-footer">'
        "Secure authentication powered by Firebase"
        "</div>",
        unsafe_allow_html=True
    )


def render_sidebar_user_panel():
    """Render the logged-in user info and logout button in the sidebar."""
    st.sidebar.markdown("---")

    # Defensive: only render if session is actually populated
    user_name = st.session_state.get("user_name", "")
    user_email = st.session_state.get("user_email", "")

    if user_name:
        st.sidebar.markdown(f"**{user_name}**")
    if user_email:
        st.sidebar.caption(user_email)

    if st.sidebar.button("Logout", use_container_width=True):
        logout_user()