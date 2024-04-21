import streamlit as st

# Bild einfügen
bild = st.image('Pfad/zum/Bild.jpg', caption='Alternativer Text')

# CSS-Stile für die Bildpositionierung
bild.markdown(
    f'<style>img.stImage {{ position: absolute; top: 0; right: 0; }}</style>',
    unsafe_allow_html=True
)


