import streamlit as st
import pandas as pd
from github_contents import GithubContents

# Set constants for fridge contents
DATA_FILE = "Kühlschrankinhalt.csv"
DATA_COLUMNS = ["Lebensmittel", "Kategorie", "Lagerort", "Ablaufdatum", "Standort"]

# Set page configuration
st.set_page_config(
    page_title="FreshAlert",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"]
        )


def init_dataframe_food():
    """Initialize or load the dataframe for user registration."""
    if 'df' not in st.session_state:
        if st.session_state.github.file_exists(DATA_FILE):
            st.session_state.df = st.session_state.github.read_df(DATA_FILE)
        else:
            st.session_state.df = pd.DataFrame(columns=DATA_COLUMNS)

def show_fresh_alert_page():
    st.title("FreshAlert")
    st.subheader("Herzlich Willkommen bei FreshAlert. Deine App für deine Lebensmittel! "            
                 "Füge links deine ersten Lebensmittel zu deinem Digitalen Kühlschrank hinzu. "
                 "Wir werden dich daran erinneren, es rechtzeitig zu benutzen und dir so helfen, keine Lebensmittel mehr zu verschwenden. "
                 "#StopFoodwaste ")
    st.sidebar.image('18-04-_2024_11-16-47.png', use_column_width=True)
    st.sidebar.title("")
    if st.sidebar.button("Mein Kühlschrank"):
        show_my_fridge_page()
    if st.sidebar.button("Neues Lebensmittel hinzufügen"):
        add_food_to_fridge()
    st.sidebar.markdown("---")  # Separator
    if st.sidebar.button("Freunde einladen"):
        show_my_friends()
    if st.sidebar.button("Einstellungen"):
        show_settings()


def show_my_fridge():
    """Display the contents of the fridge."""
    st.title("Mein Kühlschrank")
    init_dataframe_food()  # Daten laden
    if not st.session_state.df.empty:
        st.dataframe(st.session_state.df)
    else:
        st.write("Der Kühlschrank ist leer.")


def add_food_to_fridge():
    st.title("Neues Lebensmittel hinzufügen")

    new_entry = {
        DATA_COLUMNS[0]: st.text_input(DATA_COLUMNS[0]), #Lebensmittel
        DATA_COLUMNS[1]: st.selectbox("Kategorie", ["Gemüse", "Obst", "Milchprodukte", "Fleisch", "Fisch", "Eier", "Getränke", "Saucen", "Getreideprodukte", "Tiefkühlprodukte"]), #Kategorie
        DATA_COLUMNS[2]: st.selectbox("Lagerort", ["Schrank", "Kühlschrank", "Tiefkühler", "offen"]), # Location
        DATA_COLUMNS[3]: st.selectbox("Standort", ["Mein Kühlschrank", "geteilter Kühlschrank"]), #area
        DATA_COLUMNS[4]: st.date_input(DATA_COLUMNS[4]), #Ablaufdatum
    }

    for key, value in new_entry.items():
        if value == "":
            st.error(f"Bitte ergänze das Feld '{key}'")
            return

    if st.button("Registrieren"):
        new_entry_df = pd.DataFrame([new_entry])
        st.session_state.df_food = pd.concat([st.session_state.df, new_entry_df], ignore_index=True)
        save_data_to_database_food()
        st.success("Lebensmittel erfolgreich hinzugefügt!")

    st.subheader("Neues Lebensmittel")
    st.write(new_entry)





def save_data_to_database_food():
    st.session_state.github.write_df(DATA_FILE, st.session_state.df_food, "Updated food data")



def show_my_friends():
    st.write("Meine Freunde")


def show_settings():
    st.write("Einstellungen")


def main():
    init_github()
    init_dataframe_food()
    show_fresh_alert_page()


if __name__ == "__main__":
    main()
