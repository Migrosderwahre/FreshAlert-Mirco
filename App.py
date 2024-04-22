import streamlit as st
import pandas as pd
from datetime import date
from github_contents import GithubContents

# Set constants
DATA_FILE = "FreshAlert"
DATA_COLUMNS = ["Vorname", "Nachname","E-Mail", "Passwort", "Passwort wiederholen"]

# Set page configuration
st.set_page_config(page_title="My Contacts", page_icon="🎂", layout="wide",  
                   initial_sidebar_state="expanded")

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])

def init_dataframe():
    """Initialize or load the dataframe."""
    if 'df' in st.session_state:
        pass
    elif st.session_state.github.file_exists(DATA_FILE):
        st.session_state.df = st.session_state.github.read_df(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

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
            show_registration_page()

def show_registration_page():
    st.title("Registrieren")
           
    new_entry = {
        DATA_COLUMNS[0]:  st.text_input(DATA_COLUMNS[0]), #Vorname
        DATA_COLUMNS[1]:  st.text_input(DATA_COLUMNS[1]), #Nachname
        DATA_COLUMNS[2]:  st.text_input(DATA_COLUMNS[2]), # E-Mail
        DATA_COLUMNS[3]:  st.text_input(DATA_COLUMNS[3],type="password"), #Passwort
        DATA_COLUMNS[4]:  st.text_input(DATA_COLUMNS[4], type="password"), #Passwort wiederholen
    }


    for key, value in new_entry.items():
        if value == "":
            st.error(f"Bitte ergänze das Feld '{key}'")
            return

    if st.button("Registrieren"):
        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.df = pd.concat([st.session_state.df, new_entry_df], ignore_index=True)
        if new_entry["Passwort"] == new_entry["Passwort wiederholen"]:
            st.success("Registrierung erfolgreich!")
            st.session_state.show_registration = False  # Setze den Status zurück
        else:
            st.error("Die Passwörter stimmen nicht überein.")
        # Save the updated DataFrame to GitHub
        name = new_entry[DATA_COLUMNS[0]]
        msg = f"Add contact '{name}' to the file {DATA_FILE}"
        st.session_state.github.write_df(DATA_FILE, st.session_state.df, msg)




def display_dataframe():
    """Display the DataFrame in the app."""
    if not st.session_state.df.empty:
        st.dataframe(st.session_state.df)
    else:
        st.write("No data to display.")
def is_user_logged_in():
    return False

def main():
  if not is_user_logged_in():
    show_login_page()
  else:
    show_fresh_alert_page()

init_github()
init_dataframe()


if __name__ == "__main__":
        main()
