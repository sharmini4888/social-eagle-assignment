import streamlit as st
import requests

st.title("Automation Demo")

if st.button("Run Automation"):
    try:
        response = requests.get(
            "http://127.0.0.1:5000/run-automation",
            timeout=20
        )

        data = response.json()

        if data["status"] == "success":
            st.success("Automation Completed")
            st.write("Website Title:", data["website_title"])
        else:
            st.error("Flask Error")
            st.write(data["message"])

    except Exception as e:
        st.error("Connection Error")
        st.write(e)
