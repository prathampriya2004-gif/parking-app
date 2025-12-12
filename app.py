import streamlit as st
import random

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="QuickPark",
    layout="centered"
)

# ================= DARK UI + CHAT ICON =================
st.markdown("""
<style>

/* ---------- BACKGROUND ---------- */
body {
    background-color: #0b0b0f;
}
.main {
    background-color: #0b0b0f;
    padding-bottom: 120px;
}

/* ---------- HEADINGS ---------- */
h1, h2, h3 {
    color: #ffffff;
    font-weight: 800;
    text-align: center;
}

/* ---------- CARD ---------- */
.card {
    background-color: #1a1a1f;
    border-radius: 18px;
    padding: 22px;
    margin-top: 20px;
    box-shadow: 0px 12px 30px rgba(0,0,0,0.7);
}

/* ---------- TEXT ---------- */
label, p, span {
    color: #e5e7eb !important;
    font-size: 15px;
}

/* ---------- INPUTS ---------- */
input, textarea, select {
    background-color: #26262c !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #3f3f46 !important;
    padding: 12px !important;
}

/* ---------- BUTTONS ---------- */
button[kind="primary"] {
    background: linear-gradient(90deg, #2563eb, #1e40af) !important;
    color: white !important;
    border-radius: 14px !important;
    font-size: 18px !important;
    padding: 14px !important;
    width: 100% !important;
    box-shadow: 0px 6px 18px rgba(37,99,235,0.4);
}

/* ---------- CHATBOT ICON ---------- */
.chatbot {
    position: fixed;
    bottom: 25px;
    right: 25px;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #2563eb, #1e40af);
    border-radius: 50%;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    color: white;
    cursor: pointer;
    z-index: 9999;
}

.chatbot:hover {
    transform: scale(1.08);
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

# ================= PAGE: REGISTRATION TYPE =================
if st.session_state.page == "register":
    st.markdown("<h1>🚗 QuickPark</h1>", unsafe_allow_html=True)
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

# ================= PAGE: OTP =================
elif st.session_state.page == "otp":
    st.markdown("<h1>🔐 Verify Phone</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    phone = st.text_input("Phone Number")

    if st.button("Send OTP"):
        st.session_state.otp = str(random.randint(1000, 9999))
        st.success(f"OTP sent (demo): {st.session_state.otp}")

    user_otp = st.text_input("Enter OTP")

    if st.button("Verify ➜"):
        if user_otp == st.session_state.otp:
            go("details")
        else:
            st.error("Incorrect OTP")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= PAGE: PERSONAL DETAILS =================
elif st.session_state.page == "details":
    st.markdown("<h1>👤 Personal Details</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    first = col1.text_input("First Name")
    last = col2.text_input("Last Name")

    email = st.text_input("Email")
    age = st.number_input("Age", 1, 100)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    city = st.text_input("City")
    nationality = st.text_input("Nationality")

    aad1 = st.file_uploader("Aadhaar Front", type=["jpg", "png"])
    aad2 = st.file_uploader("Aadhaar Back", type=["jpg", "png"])

    if st.button("Continue ➜"):
        if st.session_state.role == "Service Seeker":
            go("seeker")
        else:
            go("provider")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= PAGE: PROVIDER =================
elif st.session_state.page == "provider":
    st.markdown("<h1>🏠 Parking Provider</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    ptype = st.selectbox(
        "Parking Type",
        ["Apartment - Owned", "Apartment - Rented", "Independent House - Owned", "Independent House - Rented"]
    )

    area = st.number_input("Parking Area (Sq. Ft.)")
    photos = st.file_uploader("Parking Photos (up to 5)", accept_multiple_files=True)
    timing = st.selectbox("Timing", ["Flexible", "Time Specific"])
    charge = st.selectbox("Monthly Charges", [1500, 2000, 2500, 3000, 3500, 4000, 4500])
    remarks = st.text_area("Remarks")

    if st.button("Submit Listing ✔"):
        st.success("Parking listed successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= PAGE: SEEKER =================
elif st.session_state.page == "seeker":
    st.markdown("<h1>🔍 Find Parking</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    ptype = st.selectbox("Parking Type", ["Apartment", "Independent House"])
    radius = st.selectbox("Distance (KM)", [1, 2, 3])
    timing = st.selectbox("Timing", ["Flexible", "Time Specific"])
    budget = st.selectbox("Budget", [1500, 2000, 2500, 3000, 3500, 4000])
    comment = st.text_area("Additional Notes")

    if st.button("Search Parking 🔍"):
        st.success("Showing parking results (demo)")

    st.markdown("</div>", unsafe_allow_html=True)
