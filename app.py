import streamlit as st
import random
from twilio.rest import Client

st.set_page_config(page_title="Parking App", layout="centered")

# ---------------- CONFIG ----------------
TWILIO_SID = "AC775ceee27f35184ad5350d70d7bd63b3"
TWILIO_AUTH = "3d51d3fa16baec3b25fdb5ad265bd5a8"
TWILIO_NUMBER = "+91 7019228583"

client = Client(TWILIO_SID, TWILIO_AUTH)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = 1
if "generated" not in st.session_state:
    st.session_state.generated = ""
if "details" not in st.session_state:
    st.session_state.details = {}

def next_page(): st.session_state.page += 1
def prev_page(): st.session_state.page -= 1

# ---------------- FUNCTION TO SEND OTP ----------------
def send_real_otp(phone, otp):
    message = client.messages.create(
        body=f"Your OTP for Parking App is: {otp}",
        from_=TWILIO_NUMBER,
        to=phone
    )
    return message.sid

# ---------------- PAGE 1 ----------------
if st.session_state.page == 1:
    st.title("📱 Registration")

    phone = st.text_input("Enter phone number (include country code)")

    if st.button("Send OTP ➡"):
        if phone.strip() == "":
            st.error("Enter a valid phone number.")
        else:
            otp = str(random.randint(1000, 9999))     # generate OTP
            st.session_state.generated = otp

            # Send OTP using Twilio
            try:
                send_real_otp(phone, otp)
                st.success("OTP sent to your phone!")
                next_page()
            except Exception as e:
                st.error("Failed to send OTP. Check Twilio setup.")
                st.write(e)

# ---------------- PAGE 2 ----------------
elif st.session_state.page == 2:
    st.title("🔐 Verify OTP")

    entered_otp = st.text_input("Enter OTP")

    col1, col2 = st.columns(2)

    if col1.button("⬅ Back"):
        prev_page()

    if col2.button("Verify ➡"):
        if entered_otp == st.session_state.generated:
            st.success("OTP verified!")
            next_page()
        else:
            st.error("Incorrect OTP")

# ---------------- PAGE 3 ----------------
elif st.session_state.page == 3:
    st.title("👤 Personal Details")

    name = st.text_input("Full Name")
    email = st.text_input("Email Address")

    col1, col2 = st.columns(2)

    if col1.button("⬅ Back"):
        prev_page()

    if col2.button("Continue ➡"):
        if name.strip() == "" or email.strip() == "":
            st.error("Please fill all fields.")
        else:
            st.session_state.details = {"name": name, "email": email}
            next_page()

# ---------------- PAGE 4 ----------------
elif st.session_state.page == 4:
    st.title("🚗 Parking Space Search")

    duration = st.selectbox("Duration", ["Hourly", "Daily", "Monthly"])
    location = st.text_input("Preferred Location")

    col1, col2 = st.columns(2)

    if col1.button("⬅ Back"):
        prev_page()

    if col2.button("Search"):
        if location.strip() == "":
            st.error("Enter a location.")
        else:
            st.success(f"Showing {duration} parking spots near {location} (demo).")
