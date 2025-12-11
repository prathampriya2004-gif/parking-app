import streamlit as st
import random

st.set_page_config(page_title="Parking App", layout="centered")

# SESSION
if "page" not in st.session_state:
    st.session_state.page = 1
if "generated" not in st.session_state:
    st.session_state.generated = ""

def next_page(): st.session_state.page += 1
def prev_page(): st.session_state.page -= 1

# PAGE 1 — Phone Number
if st.session_state.page == 1:
    st.title("📱 Registration")
    phone = st.text_input("Enter phone number")

    if st.button("Send OTP ➡"):
        if not phone:
            st.error("Enter a valid number.")
        else:
            otp = str(random.randint(1000, 9999))
            st.session_state.generated = otp
            st.success(f"OTP sent! (demo OTP: {otp})")
            next_page()

# PAGE 2 — OTP Verification
elif st.session_state.page == 2:
    st.title("🔐 Verify OTP")

    otp = st.text_input("Enter OTP")

    col1, col2 = st.columns(2)
    if col1.button("⬅ Back"): prev_page()

    if col2.button("Verify ➡"):
        if otp == st.session_state.generated:
            st.success("OTP verified!")
            next_page()
        else:
            st.error("Incorrect OTP")

# PAGE 3 — Personal Details
elif st.session_state.page == 3:
    st.title("👤 Personal Details")

    name = st.text_input("Full Name")
    email = st.text_input("Email")

    col1, col2 = st.columns(2)
    if col1.button("⬅ Back"): prev_page()

    if col2.button("Continue ➡"):
        if name and email:
            st.session_state.details = {"name": name, "email": email}
            next_page()
        else:
            st.error("Fill all details")

# PAGE 4 — Parking Search
elif st.session_state.page == 4:
    st.title("🚗 Parking Space Search")

    duration = st.selectbox("Duration", ["Hourly", "Daily", "Monthly"])
    location = st.text_input("Preferred Location")

    col1, col2 = st.columns(2)
    if col1.button("⬅ Back"): prev_page()

    if col2.button("Search"):
        if location:
            st.success(f"Showing {duration} parking near {location} (demo)")
        else:
            st.error("Enter location.")

