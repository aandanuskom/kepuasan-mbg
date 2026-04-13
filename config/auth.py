import streamlit as st

# =====================
# INIT SESSION GLOBAL
# =====================
def init_session():

    if "login" not in st.session_state:

        st.session_state.login = False

    if "username" not in st.session_state:

        st.session_state.username = None


# =====================
# CEK LOGIN
# =====================
def require_login():

    init_session()

    if not st.session_state.login:

        st.warning("Silakan login terlebih dahulu")

        st.stop()


# =====================
# LOGOUT
# =====================
def logout():

    st.session_state.login = False

    st.session_state.username = None

    st.rerun()