import streamlit as st
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Constants
DATABASE_URL = "sqlite:///user_database.db"

# Set up SQLite database
engine = create_engine(DATABASE_URL)
metadata = MetaData()
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String),
)
metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Function to check if a user exists in the database
def user_exists(username):
    with Session() as session:
        return session.query(users_table).filter_by(username=username).first() is not None

# Function to get user details
def get_user_details(username):
    with Session() as session:
        user = session.query(users_table).filter_by(username=username).first()
        return user

# Function to add a new user to the database
def add_user(username, password):
    with Session() as session:
        new_user = users_table.insert().values(username=username, password=password)
        session.execute(new_user)
        session.commit()

# Function to authenticate user credentials
def authenticate(username, password):
    with Session() as session:
        user = session.query(users_table).filter_by(username=username, password=password).first()
        return user is not None

# Streamlit app
def main():
    st.title("User Login and Registration App")

    # Sidebar with icons for registration and login
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Select Page", ["Register", "Login"])

    if selected_page == "Register":
        st.subheader("Registration")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password", key="new_password")
        register_button = st.button("Register")

        if register_button:
            if not user_exists(new_username):
                add_user(new_username, new_password)
                st.success("Registration successful! You can now log in.")
            else:
                st.warning("Username already exists. Please choose a different one.")

    elif selected_page == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password", key="password")
        login_button = st.button("Login")

        if login_button:
            if authenticate(username, password):
                st.success("Login successful!")
                
                # Get user details
                user = get_user_details(username)
                
                # Display username and password
                st.markdown(f"## Welcome, {user['username']}! 😊")
                
            else:
                st.error("Invalid credentials. Please try again.")

if __name__ == "__main__":
    main()