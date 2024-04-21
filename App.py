import streamlit as st

# Bild einfügen
bild = st.image('18-04-_2024_11-16-47.png', caption='Test')

# CSS-Stile für die Bildpositionierung
bild.markdown(
    f'<style>img.stImage {{ position: absolute; top: 0; right: 0; }}</style>',
    unsafe_allow_html=True
)


