import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from scraped_cpso import main

# Function to be executed when the "Run" button is clicked
def run_button_click():
    main()
    label.config(text="Data scraped and added to Google Sheet.")

# Function to be executed when the "Stop" button is clicked
def stop_button_click():
    label.config(text="Stopped.")

# Create the main application window
app = tk.Tk()
app.title("CPSO")

# Set the initial size of the frame (width x height)
app.geometry("600x500")

# Create a label widget
label = tk.Label(app, text="Welcome to CPSO Scrapper")
label.pack()

# Create a "Run" button
run_button = tk.Button(app, text="Run", command=run_button_click, bg="green")
run_button.place(relx=0.5, rely=0.5, anchor="c")

# Create a "Stop" button
stop_button = tk.Button(app, text="Stop", command=stop_button_click, bg="red")
stop_button.place(relx=0.5, rely=0.6, anchor="c")

# Run the application
app.mainloop()
