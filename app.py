import streamlit as st
import random
import os
from twilio.rest import Client

# --------------------------- TWILIO SETUP ---------------------------
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

client = Client(TWILIO_SID, TWILIO_AUTH)

def send_otp(phone, otp):
    try:
        client.messages.create(
            body=f"Your Parking App OTP is: {otp}",
            from_=TWILIO_NUMBER,
            to=phone
        )
        return True
    except Exception as e:
        st.error("Failed to send OTP. Check Twilio setup.")
        st.write(e)
        return False


# --------------------------- SESSION SETUP ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "registration_type"

if "selected_type" not in st.session_state:
    st.session_state.selected_type = None

if "otp_generated" not in st.session_state:
    st.session_state.otp_generated = ""


# --------------------------- PAGE NAVIGATION ---------------------------
def go(page):
    st.session_state.page = page


# --------------------------- REGISTRATION TYPE PAGE ---------------------------
if st.session_state.page == "registration_type":
    st.title("🏷 Registration Type")

    st.session_state.selected_type = st.radio(
        "Select who you are:",
        [
            "Individual Service Provider",
            "Commercial Service Provider",
            "Service Seeker"
        ]
    )

    if st.button("Next ➡"):
        go("otp")


# --------------------------- OTP PAGE ---------------------------
elif st.session_state.page == "otp":
    st.title("🔐 OTP Authentication")

    phone = st.text_input("Mobile Number (with country code)")

    if st.session_state.otp_generated == "":
        if st.button("Send OTP"):
            otp = str(random.randint(1000, 9999))
            st.session_state.otp_generated = otp

            if send_otp(phone, otp):
                st.success("OTP sent! Please check your phone.")

    entered_otp = st.text_input("Enter OTP")

    if st.button("Submit OTP"):
        if entered_otp == st.session_state.otp_generated:
            st.success("OTP Verified")
            go("personal_details")
        else:
            st.error("Incorrect OTP")


# --------------------------- PERSONAL DETAILS PAGE ---------------------------
elif st.session_state.page == "personal_details":
    st.title("👤 Personal Details")

    first = st.text_input("First Name")
    last = st.text_input("Last Name")
    email = st.text_input("Email ID")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    city = st.text_input("City")
    nationality = st.text_input("Nationality")
    aadhaar_front = st.file_uploader("Upload Aadhaar Front", type=["jpg", "png"])
    aadhaar_back = st.file_uploader("Upload Aadhaar Back", type=["jpg", "png"])

    if st.button("Continue ➡"):
        if st.session_state.selected_type == "Individual Service Provider":
            go("service_provider")
        elif st.session_state.selected_type == "Service Seeker":
            go("service_seeker")
        else:
            st.success("Commercial Provider module coming soon!")


# --------------------------- INDIVIDUAL SERVICE PROVIDER PAGE ---------------------------
elif st.session_state.page == "service_provider":
    st.title("🏠 Individual Service Provider")

    parking_type = st.selectbox(
        "Parking Type",
        [
            "Apartment - Owned",
            "Apartment - Rented",
            "Independent House - Owned",
            "Independent House - Rented"
        ]
    )

    square_ft = st.number_input("Parking Area (Sq. Ft)")

    st.subheader("Upload Parking Photos (up to 5)")
    photos = st.file_uploader("Select Photos", accept_multiple_files=True)

    timing = st.selectbox(
        "Timing Flexibility",
        ["Flexible", "Time-Specific"]
    )

    charges = st.selectbox(
        "Per Month Charges (₹)",
        [1500, 2000, 2500, 3000, 3500, 4000, 4500]
    )

    remarks = st.text_area("Remarks")

    if st.button("Submit Details"):
        st.success("Details submitted successfully! 🎉")


# --------------------------- SERVICE SEEKER PAGE ---------------------------
elif st.session_state.page == "service_seeker":
    st.title("🔍 Looking for Parking Space")

    parking_type = st.selectbox("Parking Type", ["Apartment", "Independent House"])
    distance = st.selectbox("Search Radius (KM)", [1, 2, 3])
    timing = st.selectbox("Timing", ["Flexible", "Time-Specific"])
    charges = st.selectbox(
        "Max Per Month Budget (₹)",
        [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500]
    )
    comment = st.text_area("Additional Comments")

    interest = st.radio(
        "Are you interested?",
        ["Interested - Show Contact Number", "Not Interested"]
    )

    pay_option = st.radio(
        "Choose Payment Option",
        [
            "₹100 per contact",
            "₹500 per contact",
            "₹800 per contact"
        ]
    )

    if st.button("Search Parking"):
        st.success("Showing parking options near you... (demo)")


# --------------------------- END ---------------------------
