import streamlit as st
import random
import os
from twilio.rest import Client

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="QuickPark",
    layout="centered"
)

# ================= TWILIO SETUP =================
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

twilio_client = None
if TWILIO_SID and TWILIO_AUTH:
    twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

def send_otp(phone, otp):
    try:
        if twilio_client:
            twilio_client.messages.create(
                body=f"Your QuickPark OTP is {otp}",
                from_=TWILIO_NUMBER,
                to=phone
            )
            return True, None
        else:
            return False, "Twilio not configured"
    except Exception as e:
        return False, str(e)

# ================= UI STYLES =================
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
body {
    background-color: #000000;
}
.main {
    background-color: #000000;
    padding-bottom: 120px;
}

/* ===== HEADINGS ===== */
h1, h2, h3 {
    color: #ffffff;
    font-weight: 800;
    text-align: center;
}

/* ===== CARD ===== */
.card {
    background-color: #121212;
    border-radius: 18px;
    padding: 24px;
    margin-top: 20px;
    border: 1px solid #2a2a2a;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.85);
}

/* ===== TEXT ===== */
label, p, span {
    color: #d1d5db !important;
    font-size: 15px;
}

/* ===== INPUTS ===== */
input, textarea, select {
    background-color: #1f1f1f !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #3a3a3a !important;
    padding: 12px !important;
}

/* ===== BUTTONS ===== */
button[kind="primary"] {
    background: linear-gradient(90deg, #2563eb, #1e40af) !important;
    color: white !important;
    border-radius: 14px !important;
    font-size: 17px !important;
    padding: 14px !important;
    width: 100% !important;
    box-shadow: 0px 6px 18px rgba(37,99,235,0.45);
}

/* ===== CHATBOT ICON ===== */
.chatbot {
    position: fixed;
    bottom: 25px;
    right: 25px;
    width: 58px;
    height: 58px;
    background: linear-gradient(135deg, #2563eb, #1e40af);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    color: white;
    cursor: pointer;
    z-index: 9999;
}
</style>

<div class="chatbot" title="Chatbot (Coming Soon)">💬</div>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "page" not in st.session_state:
    st.session_state.page = "register"

if "otp" not in st.session_state:
    st.session_state.otp = ""

def go(page):
    st.session_state.page = page

# ================= HEADER =================
st.markdown("<h1>🚗 QuickPark</h1>", unsafe_allow_html=True)

# ================= NAV =================
c1, c2, c3 = st.columns(3)
if c1.button("🏠 Home"):
    go("register")
if c2.button("📞 Contact"):
    go("contact")
if c3.button("ℹ️ About"):
    go("about")

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
    st.subheader("🔐 Verify Phone Number")

    phone = st.text_input("Phone Number (with country code)")

    if st.button("Send OTP"):
        st.session_state.otp = str(random.randint(1000, 9999))
        ok, err = send_otp(phone, st.session_state.otp)
        if ok:
            st.success("OTP sent to your phone")
        else:
            st.warning("OTP could not be sent via SMS.")
            st.info(f"Demo OTP (for testing): {st.session_state.otp}")
            if err:
                st.caption(err)

    user_otp = st.text_input("Enter OTP")

    if st.button("Verify ➜"):
        if user_otp == st.session_state.otp:
            go("details")
        else:
            st.error("Incorrect OTP")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= DETAILS =================
elif st.session_state.page == "details":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👤 Personal Details")

    col1, col2 = st.columns(2)
    col1.text_input("First Name")
    col2.text_input("Last Name")

    st.text_input("Email")
    st.number_input("Age", 1, 100)
    st.selectbox("Gender", ["Male", "Female", "Other"])
    st.text_input("City")
    st.text_input("Nationality")

    if st.button("Continue ➜"):
        if st.session_state.role == "Service Seeker":
            go("seeker")
        else:
            go("provider")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= PROVIDER =================
elif st.session_state.page == "provider":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏠 Parking Provider")

    st.selectbox(
        "Parking Type",
        ["Apartment - Owned", "Apartment - Rented",
         "Independent House - Owned", "Independent House - Rented"]
    )

    st.number_input("Parking Area (Sq. Ft.)")
    st.file_uploader("Parking Photos", accept_multiple_files=True)
    st.selectbox("Timing", ["Flexible", "Time Specific"])
    st.selectbox("Monthly Charges",
                 [1500, 2000, 2500, 3000, 3500, 4000, 4500])
    st.text_area("Remarks")

    if st.button("Submit Listing"):
        st.success("Parking listed successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= SEEKER =================
elif st.session_state.page == "seeker":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔍 Find Parking")

    st.selectbox("Parking Type", ["Apartment", "Independent House"])
    st.selectbox("Distance (KM)", [1, 2, 3])
    st.selectbox("Timing", ["Flexible", "Time Specific"])
    st.selectbox("Budget",
                 [1500, 2000, 2500, 3000, 3500, 4000])
    st.text_area("Additional Notes")

    if st.button("Search Parking"):
        st.success("Showing parking results (demo)")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= CONTACT =================
elif st.session_state.page == "contact":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📞 Contact Us")

    st.markdown("""
    **👤 Founder**  
    **Suman Raju**

    **📞 Phone**  
    +91-80-9986575103
    """)

    st.markdown("---")
    st.subheader("✉️ Send us a message")

    st.text_input("Your Name")
    st.text_input("Your Email")
    st.text_area("Message")

    if st.button("Send Message"):
        st.success("Thank you! We’ll get back to you soon.")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= ABOUT =================
elif st.session_state.page == "about":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("ℹ️ About QuickPark")

    st.write("""
    QuickPark helps people easily find and provide parking spaces.

    • List your parking space  
    • Find parking near you  
    • Simple, fast & secure  

    Built with ❤️ using Streamlit.
    """)

    st.markdown("</div>", unsafe_allow_html=True)
