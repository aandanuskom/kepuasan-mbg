import streamlit as st

# =====================
# NAVBAR
# =====================
def navbar():

    col1,col2 = st.columns([8,1])

    with col1:
        st.markdown(
            """
            <h3 style='margin-top:5px'>
            Sistem Analisis Kepuasan MBG
            </h3>
            """,
            unsafe_allow_html=True
        )

    with col2:

        if st.button("Logout"):

            st.session_state.login = False

            st.rerun()

    st.divider()


# =====================
# FOOTER
# =====================
def footer():

    st.divider()

    st.markdown(
        """
        <div style='text-align:center;
        color:gray;
        font-size:14px'>

        © 2026 Sistem Kepuasan MBG
        <br>
        Metode Support Vector Machine (SVM)

        </div>
        """,
        unsafe_allow_html=True
    )