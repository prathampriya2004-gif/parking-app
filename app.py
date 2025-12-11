import streamlit as st
import random
import os
from twilio.rest import Client


# -----------------------------------------------------------
# TWILIO SETUP (REAL OTP)
# -----------------------------------------------------------
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_real_otp(phone, otp):
    try:
        client.messages.create(
            body=f"Your Parking App OTP is {otp}",
            from_=TWILIO_NUMBER,
            to=phone
        )
        return True
    except Exception as e:
        st.error("❌ OTP sending failed.")
        st.write(e)
        return False


# -----------------------------------------------------------
# PAGE CONFIG + CUSTOM UI
# -----------------------------------------------------------
st.set_page_config(page_title="Smart Parking App", layout="centered")

st.markdown("""
<style>

body {
    background: linear-gradient(150deg, #3c1053, #ad5389);
    color: white !important;
}

.main {
    background: transparent;
}

h1, h2, h3, label, p, span {
    color: white !important;
}

/* GLASS CARD */
.glass-card {
    background: rgba(255, 255, 255, 0.18);
    border-radius: 18px;
    padding: 25px 25px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255, 255, 255, 0.28);
    margin-top: 20px;
    box-shadow: 0 8px 35px rgba(0,0,0,0.25);
}

/* BUTTONS */
button[kind="primary"] {
    background: linear-gradient(90deg, #ff5f6d, #ffc371) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    font-size: 18px !important;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

/* TEXT INPUTS */
input, textarea, select {
    border-radius: 10px !important;
}

/* TITLE */
.fancy-title {
    font-size: 38px !important;
    text-align: center;
    font-weight: 900;
    text-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------
# SESSION
# -----------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "registration_type"

if "selected_type" not in st.session_state:
    st.session_state.selected_type = None

if "otp_generated" not in st.session_state:
    st.session_state.otp_generated = None

def go(p): st.session_state.page = p


# -----------------------------------------------------------
# PAGE: REGISTRATION TYPE
# -----------------------------------------------------------
if st.session_state.page == "registration_type":
    st.markdown("<h1 class='fancy-title'>🚗 Smart Parking App</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    st.subheader("Choose Your Role")

    st.session_state.selected_type = st.radio(
        "",
        ["Individual Service Provider", "Commercial Service Provider", "Service Seeker"]
    )

    if st.button("Next ➜"):
        go("otp")

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------
# PAGE: OTP
# -----------------------------------------------------------
elif st.session_state.page == "otp":
    st.markdown("<h1 class='fancy-title'>🔐 Verify Your Number</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    phone = st.text_input("Enter Phone Number (with country code)")

    if st.button("Send OTP"):
        otp = str(random.randint(1000, 9999))
        st.session_state.otp_generated = otp

        if send_real_otp(phone, otp):
            st.success("OTP sent to your phone ✔")
        else:
            st.error("OTP failed. Check Twilio region restrictions.")

    user_otp = st.text_input("Enter OTP")

    if st.button("Verify ➜"):
        if user_otp == st.session_state.otp_generated:
            st.success("OTP Verified ✔")
            go("details")
        else:
            st.error("Incorrect OTP ❌")

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------
# PAGE: PERSONAL DETAILS
# -----------------------------------------------------------
elif st.session_state.page == "details":
    st.markdown("<h1 class='fancy-title'>👤 Personal Details</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    first = col1.text_input("First Name")
    last = col2.text_input("Last Name")

    email = st.text_input("Email ID")
    age = st.number_input("Age", 1, 100)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    city = st.text_input("City")
    nationality = st.text_input("Nationality")

    aadhaar_front = st.file_uploader("Upload Aadhaar Front", type=["jpg","png"])
    aadhaar_back = st.file_uploader("Upload Aadhaar Back", type=["jpg","png"])

    if st.button("Continue ➜"):
        if st.session_state.selected_type == "Individual Service Provider":
            go("provider")
        else:
            go("seeker")

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------
# PAGE: INDIVIDUAL PROVIDER
# -----------------------------------------------------------
elif st.session_state.page == "provider":
    st.markdown("<h1 class='fancy-title'>🏠 Parking Provider</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    parking_type = st.selectbox(
        "Parking Type",
        ["Apartment - Owned", "Apartment - Rented", "Independent House - Owned", "Independent House - Rented"]
    )

    size = st.number_input("Parking Area (Sq. Ft.)")

    photos = st.file_uploader("Upload Parking Photos (up to 5)", accept_multiple_files=True)

    timing = st.selectbox("Timing Flexibility", ["Flexible", "Time-Specific"])

    charges = st.selectbox("Monthly Charges", [1500,2000,2500,3000,3500,4000,4500])

    remarks = st.text_area("Remarks")

    if st.button("Submit Details ✔"):
        st.success("Parking details submitted successfully! 🎉")

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------------
# PAGE: SERVICE SEEKER
# -----------------------------------------------------------
elif st.session_state.page == "seeker":
    st.markdown("<h1 class='fancy-title'>🔍 Find Parking</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    type_sel = st.selectbox("Parking Type", ["Apartment", "Independent House"])
    radius = st.selectbox("Search Radius (KM)", [1,2,3])
    timing = st.selectbox("Timing", ["Flexible", "Time-Specific"])
    budget = st.selectbox("Max Budget (₹)", [1500,2000,2500,3000,3500,4000])

    comment = st.text_area("Additional Comments")

    if st.button("Search Now 🔎"):
        st.success("Showing best parking options near you... (demo)")

    st.markdown("</div>", unsafe_allow_html=True)
