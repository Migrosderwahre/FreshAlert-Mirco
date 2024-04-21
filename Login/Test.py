def main():
    if not is_user_logged_in():
        show_login_page()
    else:
        show_fresh_alert_page()
def is_user_logged_in():
    return True  # Für dieses Beispiel gehe ich davon aus, dass der Benutzer nicht eingeloggt ist
    
def show_login_page():
    st.title("Login")
    email = st.text_input("E-Mail", key="login_email")
    password = st.text_input("Passwort", type="password", key="login_password")
    if st.button("Login"):
        if email == "example@example.com" and password == "password":
            st.success("Erfolgreich eingeloggt!")
            show_fresh_alert_page()
        else:
            st.error("Ungültige E-Mail oder Passwort.")
    if st.button("Registrieren", key="registration_button"):
        st.session_state.show_registration = True
    if st.session_state.get("show_registration", False):
        with st.sidebar:
            show_registration_page()

def show_registration_page():
    st.title("Registrieren")
    first_name = st.text_input("Vorname", key="register_first_name")
    last_name = st.text_input("Nachname", key="register_last_name")
    email = st.text_input("E-Mail", key="register_email")
    password = st.text_input("Passwort", type="password", key="register_password")
    confirm_password = st.text_input("Passwort wiederholen", type="password", key="confirm_register_password")
   # Registrierungs-Button
    if st.button("Registrieren"):
        if password == confirm_password:
            st.success("Registrierung erfolgreich!")
            st.session_state.show_registration = False  # Setze den Status zurück
        else:
            st.error("Die Passwörter stimmen nicht überein.")

if __name__ == "__main__":

    main()
