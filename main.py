import streamlit as st

from streamlit_option_menu import option_menu

import invoice, resume, account
# st.set_page_config(page_title="DocHub", page_icon="🌌", layout="wide")

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })
    def run():
        with st.sidebar:
            app = option_menu(
                menu_title = "Go to",
                options = ['account','invoice','resume'],
                # icons = ['file-invoice-dollar', 'file-alt'],
                menu_icon = 'person-circle',
                default_index = 0,
            )
        if app == 'invoice':
            invoice.app()
        if app == 'resume':
            resume.app()
        if app == 'account':
            account.app()
    run()