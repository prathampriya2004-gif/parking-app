import streamlit as st
import random
import os
from twilio.rest import Client

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="QuickPark",
    layout="centered"
)

# ================= AESTHETIC UI THEME =================
st.markdown("""
<style>

/* ===== GLOBAL BACKGROUND ===== */
html, body, .stApp {
    background: linear-gradient(180deg, #0f172a, #020617) !important;
}

/* Remove white containers */
.main, .block-container {
    background: transparent !important;
    padding-top: 2rem;
    padding-bottom: 8rem;
}

/* ===== HEADINGS ===== */
h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 800;
    text-align: center;
}

/* ===== CARDS ===== */
.card {
    background: #111827;
    border-radius: 20px;
    padding: 26px;
    margin-top: 22px;
    border: 1px solid #1f2933;
    box-shadow: 0 20px 40px rgba(0,0,0,0.6);
}

/* ===== TEXT ===== */
label, p, span, div {
    color: #e5e7eb !important;
    font-size: 15px;
}

/* ===== INPUTS ===== */
input, textarea, select {
    background-color: #020617 !important;
    color: #f8fafc !important;
    border-radius: 14px !important;
    border: 1px solid #334155 !important;
    padding: 14px !important;
}

/* ===== PRIMARY BUTTON ===== */
button[kind="primary"] {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border-radius: 16px !important;
    font-size: 17px !important;
    padding: 14px !important;
    width: 100% !important;
    border: none !important;
    box-shadow: 0px 8px 22px rgba(139,92,246,0.5);
}

/* ===== NAV BUTTONS ===== */
button {
    border-radius: 14px !important;
}

/* ===== CHATBOT ICON ===== */
.chatbot {
    position: fixed;
    bottom: 26px;
    right: 26px;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    color: white;
    cursor: pointer;
    z-index: 9999;
    box-shadow: 0 10px 30px rgba(99,102,241,0.6);
}

</style>

<div class="chatbot" title="Chatbot (Coming Soon)">💬</div>
""", unsafe_allow_html=True)

# ================= TWILIO =================
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

twilio_client = Client(TWILIO_SID, TWILIO_AUTH) if TWILIO_SID else None

def send_otp(phone, otp):
    try:
        if twilio_client:
            twilio_client.messages.create(
                body=f"Your QuickPark OTP is {otp}",
                from_=TWILIO_NUMBER,
                to=phone
            )
            return True
    except:
        pass
    return False

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "register"
if "otp" not in st.session_state:
    st.session_state.otp = ""

def go(p):
    st.session_state.page = p

# ================= HEADER =================
st.markdown("<h1>🚗 QuickPark</h1>", unsafe_allow_html=True)

# ================= NAV =================
c1, c2, c3 = st.columns(3)
if c1.button("🏠 Home"): go("register")
if c2.button("📞 Contact"): go("contact")
if c3.button("ℹ️ About"): go("about")

# ================= REGISTER =================
if st.session_state.page == "register":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Choose Your Role")

    role = st.radio(
        "",
        ["Individual Service Provider", "Commercial Service Provider", "Service Seeker"]
    )

    if st.button("Continue ➜"):
        st.session_state.role = role
        go("otp")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= OTP =================
elif st.session_state.page == "otp":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔐 Phone Verification")

    phone = st.text_input("Phone Number (with country code)")

    if st.button("Send OTP"):
        st.session_state.otp = str(random.randint(1000, 9999))
        if send_otp(phone, st.session_state.otp):
            st.success("OTP sent successfully")
        else:
            st.info(f"Demo OTP: {st.session_state.otp}")

    user_otp = st.text_input("Enter OTP")

    if st.button("Verify ➜"):
        if user_otp == st.session_state.otp:
            go("details")
        else:
            st.error("Invalid OTP")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= DETAILS =================
elif st.session_state.page == "details":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👤 Personal Details")

    c1, c2 = st.columns(2)
    c1.text_input("First Name")
    c2.text_input("Last Name")

    st.text_input("Email")
    st.number_input("Age", 1, 100)
    st.selectbox("Gender", ["Male", "Female", "Other"])
    st.text_input("City")

    if st.button("Continue ➜"):
        go("provider" if st.session_state.role != "Service Seeker" else "seeker")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= PROVIDER =================
elif st.session_state.page == "provider":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏠 Parking Provider")

    st.selectbox("Parking Type", [
        "Apartment - Owned", "Apartment - Rented",
        "Independent House - Owned", "Independent House - Rented"
    ])

    st.number_input("Parking Area (Sq. Ft.)")
    st.selectbox("Timing", ["Flexible", "Time Specific"])
    st.selectbox("Monthly Charges", [1500,2000,2500,3000,3500,4000])

    if st.button("Submit Listing"):
        st.success("Parking listed successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= SEEKER =================
elif st.session_state.page == "seeker":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔍 Find Parking")

    st.selectbox("Parking Type", ["Apartment", "Independent House"])
    st.selectbox("Distance (KM)", [1,2,3])
    st.selectbox("Budget", [1500,2000,2500,3000,3500])

    if st.button("Search Parking"):
        st.success("Results loaded (demo)")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= CONTACT =================
elif st.session_state.page == "contact":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📞 Contact Us")

    st.markdown("""
    **👤 Founder**  
    **Suman Raju**  

    **📱 Phone**  
    +91-80-9986575103
    """)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= ABOUT =================
elif st.session_state.page == "about":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("ℹ️ About QuickPark")

    st.write("""
    QuickPark helps people easily list and find parking spaces.
    A modern, secure, and easy-to-use parking solution.
    """)

    st.markdown("</div>", unsafe_allow_html=True)
