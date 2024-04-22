import streamlit as st
import pandas as pd
from github_contents import GithubContents

# Set constants
DATA_FILE = "FreshAlert-Registration"
DATA_COLUMNS = ["Vorname", "Nachname", "E-Mail", "Passwort", "Passwort wiederholen"]

DATA_FILE_FOOD = "FridgeContents.csv"
DATA_COLUMNS_FOOD = ["Lebensmittel", "Kategorie", "Lagerort", "Ablaufdatum"]

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
    if 'df' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

def show_login_page():
    st.title("Login")
    email = st.text_input("E-Mail", key="login_email")
    password = st.text_input("Passwort", type="password", key="login_password")
    if st.button("Login"):
        login_successful = False
        for index, row in st.session_state.df.iterrows():
            if row["E-Mail"] == email and row["Passwort"] == password:
                login_successful = True
                break
        if login_successful:
            st.session_state.user_logged_in = True
            st.success("Erfolgreich eingeloggt!")
        else:
            st.error("Ungültige E-Mail oder Passwort.")
    if st.button("Registrieren", key="registration_button"):
        st.session_state.show_registration = True
    if st.session_state.get("show_registration", False):
        show_registration_page()

def show_registration_page():
    st.title("Registrieren")
           
    new_entry = {
        DATA_COLUMNS[0]: st.text_input(DATA_COLUMNS[0]), #Vorname
        DATA_COLUMNS[1]: st.text_input(DATA_COLUMNS[1]), #Nachname
        DATA_COLUMNS[2]: st.text_input(DATA_COLUMNS[2]), # E-Mail
        DATA_COLUMNS[3]: st.text_input(DATA_COLUMNS[3], type="password"), #Passwort
        DATA_COLUMNS[4]: st.text_input(DATA_COLUMNS[4], type="password"), #Passwort wiederholen
    }

    for key, value in new_entry.items():
        if value == "":
            st.error(f"Bitte ergänze das Feld '{key}'")
            return

    if st.button("Registrieren"):
        if new_entry["Passwort"] == new_entry["Passwort wiederholen"]:
            new_entry_df = pd.DataFrame([new_entry])
            st.session_state.df = pd.concat([st.session_state.df, new_entry_df], ignore_index=True)
            save_data_to_database_login()
            st.success("Registrierung erfolgreich!")
            st.session_state.show_registration = False  # Setze den Status zurück
        else:
            st.error("Die Passwörter stimmen nicht überein.")

def show_fresh_alert_page():
    st.title("FreshAlert")
    st.sidebar.image('18-04-_2024_11-16-47.png', use_column_width=True)
    st.sidebar.title("")
    if st.sidebar.button("Mein Kühlschrank"):
        show_my_fridge()
    if st.sidebar.button("Neues Lebensmittel hinzufügen"):
        add_new_food()
    st.sidebar.markdown("---")  # Trennlinie
    if st.sidebar.button("Freunde einladen"):
        show_my_friends()
    if st.sidebar.button("Einstellungen"):
        show_settings()
def show_frige_page():
    st.title("Essen yeah")
           
    new_entry = {
        DATA_COLUMNS_FOOD[0]: st.text_input(DATA_COLUMNS_FOOD[0]), #Lebensmittel
        DATA_COLUMNS_FOOD[1]: st.text_input(DATA_COLUMNS_FOOD[1]), #Kategorie
        DATA_COLUMNS_FOOD[2]: st.text_input(DATA_COLUMNS_FOOD[2]), # Lagerort
        DATA_COLUMNS_FOOD[3]: st.text_input(DATA_COLUMNS_FOOD[3]), # Ablaufdatum
    }
def display_fridge_contents():
    """Display the contents of the fridge."""
    st.title("Mein Kühlschrank")
    if not st.session_state.df.empty:
        st.dataframe(st.session_state.df)
    else:
        st.write("Der Kühlschrank ist leer.")
      
def add_food_to_fridge():
    """Add a new food item to the fridge."""
    st.title("Neues Lebensmittel hinzufügen")
    with st.form("new_food_form"):
        st.write("Füllen Sie die folgenden Felder aus:")
        food_name = st.text_input("Lebensmittel")
        category = st.selectbox("Kategorie", ["Gemüse", "Obst", "Milchprodukte", "Fleisch", "Fisch", "Eier", "Getränke", "Saucen", "Getreideprodukte", "Tiefkühlprodukte"])
        location = st.selectbox("Lagerort", ["Schrank", "Kühlschrank", "Tiefkühler", "offen"])
        expiry_date = st.date_input("Ablaufdatum")
        submitted = st.form_submit_button("Hinzufügen")
        if submitted:
            new_entry = pd.DataFrame([[food_name, category, location, expiry_date]], columns=DATA_COLUMNS_FOOD)
            st.session_state.df = pd.concat([st.session_state.df, new_entry], ignore_index=True)
            st.session_state.github.write_df(DATA_FILE, st.session_state.df, "Updated fridge contents")
            st.success("Lebensmittel erfolgreich hinzugefügt!")

def show_my_friends():
    st.write("Meine Freunde")

def show_settings():
    st.write("Einstellungen")

def save_data_to_database_login():
    # Speichere die aktualisierte DataFrame in der Datenbank
    st.session_state.github.write_df(DATA_FILE, st.session_state.df, "Updated registration data")

def save_data_to_database_food():
    # Speichern Sie die Daten in der Datenbank
    if 'github' in st.session_state:
        st.session_state.github.write_df(DATA_FILE, st.session_state.df, "Updated food data")

def main():
    init_github()
    init_dataframe()
    add_food_to_fridge()
    display_fridge_contents()
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False

    if not st.session_state.user_logged_in:
        show_login_page()
    else:
        show_fresh_alert_page()

if __name__ == "__main__":
    main()
