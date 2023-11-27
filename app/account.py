# account.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, storage

def signout():
    st.session_state.signout = False
    st.session_state.signedout = True  # Set to True to indicate user has signed out
    st.session_state.username = ''
    st.session_state.login_successful = False  # Reset the login_successful flag
    st.success('Gracias por utilizar LernIA')  # Display the logout message

def account():
    st.title('Lern.IA - asistente virtual')

# Inserting the centered and justified text at the top of the account page
    st.markdown("""
        <style>
        .justified-text {
            text-align: justify;
            text-justify: inter-word;
        }
        </style>
        <div class="justified-text">
        La app Learn.IA, basada en inteligencia artificial, optimiza el diseño instruccional al ayudar a crear resultados de aprendizaje y proponer indicadores de logro y metodologías de aprendizaje activo. Los usuarios seleccionan el nombre de la asignatura, su contenido y campo de conocimiento según CINE 2013. La app proporciona propuestas de resultados de aprendizaje basadas en la taxonomía SOLO y sugiere indicadores de logro según los estándares de Quality Matters, además de metodologías de aprendizaje activo centradas en los estudiantes. Los usuarios pueden adaptar estas sugerencias para enriquecer el syllabus de su asignatura, adecuándolo al nivel deseado de conocimiento y profundidad.<br><br>
        
        </div>
        """, unsafe_allow_html=True)

    st.write("___" * 34)
    
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def login_user():
        email = st.session_state['login_email']
        password = st.session_state['login_password']
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True
            st.session_state.login_successful = True
        except:
            st.warning('Login Failed')
            st.session_state.login_successful = False

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    if not st.session_state["signedout"]: 
        login_tab, signup_tab = st.tabs(['Login', 'Sign up'])

        with login_tab:
            email = st.text_input('Email Address', key='login_email')
            password = st.text_input('Password', type='password', key='login_password')
            if st.button('Login', on_click=login_user):
                pass  # The callback function 'login_user' is now used

        with signup_tab:
            email = st.text_input('Email Address', key='signup_email')
            password = st.text_input('Password', type='password', key='signup_password')
            confirm_password = st.text_input('Confirm Password', type='password', key='signup_confirm_password')
            if st.button('Crear cuenta'):
                if password == confirm_password:
                    try:
                        user = auth.create_user(email=email, password=password)
                        st.success('Cuenta creada exitosamente')
                        st.markdown('Ingresar con email y password') 
                    except Exception as e:
                        st.error(f"Error creating user: {e}")
                else:
                    st.error("Passwords do not match")




            
        

        



