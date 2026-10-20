
import os
from pathlib import Path
from configparser import ConfigParser

import streamlit as st


def config():
    # First: use Streamlit secrets when deployed
    try:
        if "postgresql" in st.secrets:
            return dict(st.secrets["postgresql"])
    except (FileNotFoundError, KeyError):
        pass

    # Second: use environment variables if configured
    env_params = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT", "5432"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }

    if all(env_params.get(key) for key in ("host", "database", "user", "password")):
        return env_params

    # Third: local development configuration
    ini_path = Path(__file__).resolve().parent / "database.ini"
    parser = ConfigParser()

    if not parser.read(ini_path):
        raise RuntimeError(
            "Database configuration is missing. "
            "Configure Streamlit secrets, environment variables, "
            "or a local database.ini file."
        )

    if not parser.has_section("postgresql"):
        raise RuntimeError(
            "The [postgresql] section is missing from database.ini."
        )

    return dict(parser.items("postgresql"))

