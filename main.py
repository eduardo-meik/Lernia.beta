# main.py
import streamlit as st
import json
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials
from app.lernia import display
from app.account import account, signout  # Importing the account module

# Set the page config at the top level
st.set_page_config(
    page_title="Lernia Beta",
    page_icon="🧊"
)

# Initialize Firebase SDK
def initialize_firebase():
    key_dict = json.loads(st.secrets["textkey"])
    creds = credentials.Certificate(key_dict)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(creds, {'storageBucket': 'pullmai-e0bb0.appspot.com'})


# Define main app function
def main():
    
    try:
        initialize_firebase()
    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Hide the footer using custom CSS
    st.markdown("""
        <style>
            footer {
                visibility: hidden;
            }
            footer:after {
                content:'Meik Labs 2023'; 
                visibility: visible;
                display: block;
                position: relative;
                padding: 5px;
                top: 2px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Check for authentication
    if not st.session_state.get("signedout", False):  # User not logged in
        account()  # This calls the account function which handles authentication
        return  # Ensures that the rest of the application doesn't run until the user is authenticated

    
    # Navigation bar Menu
    selected = option_menu(
        menu_title=None,  # menu title
        options=['Inicio', 'Salir'],  # menu options
        icons=['layers', 'box-arrow-in-right'],  # menu icons
        menu_icon="cast",  # menu icon
        default_index=0,  # default selected index
        orientation="horizontal"  # sidebar or navigation bar
    )

    if selected == "Inicio":
        st.title("Learn.IA, Asistente Virtual Instruccional")
        display()
    elif selected == "Salir":
        signout()
   
if __name__ == "__main__":
    main()