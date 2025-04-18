import tkinter as tk
import requests
import random
import threading
import websocket
import json
import time
import logging

# Setup logging configuration
logging.basicConfig(filename="game.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Blockchain.com WebSocket URL
WS_URL = "wss://ws.blockchain.info/inv"
SATOSHIS_PER_BTC = 100_000_000  # 1 BTC = 100,000,000 satoshis

class HighLowGameGUI:
    """Class to create a High or Low BTC Game with transaction history tracking."""
    def __init__(self, root):
        self.root = root
        self.root.title("High or Low BTC Game")
        self.root.geometry("500x500")  # Adjusted window size for history panel

        self.balance = 0  # Start with 0 BTC
        self.deposit_address = self.generate_btc_address()  # Generate deposit address
        logging.info(f"Generated BTC deposit address: {self.deposit_address}")

        # Balance Display
        balance_frame = tk.Frame(root, bd=2, relief="sunken")
        balance_frame.pack(pady=5)
        self.balance_label = tk.Label(balance_frame, text=f"Balance: {self.balance:.8f} BTC", font=("Arial", 14), width=30, anchor="w")
        self.balance_label.pack()

        # Deposit Address Display
        self.address_label = tk.Label(root, text=f"Deposit BTC to: {self.deposit_address}", font=("Arial", 12), fg="blue")
        self.address_label.pack()

        # Betting Section
        self.bet_entry = tk.Entry(root)
        self.bet_entry.insert(0, "0.00000001")  # Default bet: 1 Satoshi
        self.bet_entry.pack()

        self.higher_button = tk.Button(root, text="Higher", font=("Arial", 12), state=tk.DISABLED, command=lambda: self.play_round("higher"))
        self.higher_button.pack(pady=5)
        self.lower_button = tk.Button(root, text="Lower", font=("Arial", 12), state=tk.DISABLED, command=lambda: self.play_round("lower"))
        self.lower_button.pack(pady=5)

        # Withdrawal Section
        self.withdraw_label = tk.Label(root, text="Withdraw BTC to:", font=("Arial", 12))
        self.withdraw_label.pack()
        self.withdraw_entry = tk.Entry(root)
        self.withdraw_entry.pack()
        self.withdraw_amount = tk.Entry(root)
        self.withdraw_amount.insert(0, "0.00000001")  # Default withdrawal amount
        self.withdraw_amount.pack()
        self.withdraw_button = tk.Button(root, text="Withdraw BTC", font=("Arial", 12), command=self.withdraw_btc)
        self.withdraw_button.pack()

        # Result Display
        self.result_label = tk.Label(root, text="Deposit BTC to start playing.", font=("Arial", 12))
        self.result_label.pack()

        # Transaction History Panel
        self.history_label = tk.Label(root, text="Transaction History:", font=("Arial", 12, "bold"))
        self.history_label.pack()
        self.history_box = tk.Text(root, height=10, width=60, wrap="word")
        self.history_box.pack()
        self.history_box.insert("end", "Game transactions will appear here...\n")
        self.history_box.config(state="disabled")

        # Start WebSocket tracking in a background thread
        threading.Thread(target=self.track_transactions, daemon=True).start()

    def update_transaction_history(self, message):
        """Update the transaction history panel with a new message."""
        self.history_box.config(state="normal")  # Enable editing
        self.history_box.insert("end", message + "\n")  # Add message
        self.history_box.config(state="disabled")  # Disable editing
        logging.info(message)  # Log transaction

    def generate_btc_address(self):
        """Generate a new Bitcoin address using Blockchain.com API."""
        try:
            url = f"https://api.blockchain.com/v3/address"
            response = requests.post(url, headers={"API-Key": "your_api_key_here"})
            if response.status_code == 200:
                return response.json()["address"]
            else:
                logging.error("Failed to generate BTC address")
                return "Error generating address"
        except Exception as e:
            logging.error(f"Unexpected error generating BTC address: {e}")
            return "Error generating address"

    def withdraw_btc(self):
        """Withdraw BTC to a player’s provided Bitcoin address."""
        try:
            recipient_address = self.withdraw_entry.get()
            amount = float(self.withdraw_amount.get())

            if amount <= 0 or amount > self.balance:
                self.result_label.config(text="Invalid withdrawal amount!")
                message = f"Invalid withdrawal attempt: {amount:.8f} BTC"
                self.update_transaction_history(message)
                return

            url = f"https://api.blockchain.com/v3/send"
            data = {"to": recipient_address, "amount": amount * SATOSHIS_PER_BTC, "currency": "BTC"}
            response = requests.post(url, json=data, headers={"API-Key": "your_api_key_here"})

            if response.status_code == 200:
                self.balance -= amount
                self.balance_label.config(text=f"Balance: {self.balance:.8f} BTC")
                self.result_label.config(text=f"Sent {amount:.8f} BTC to {recipient_address}!")
                message = f"Withdrawn {amount:.8f} BTC to {recipient_address}"
                self.update_transaction_history(message)
            else:
                self.result_label.config(text="Withdrawal failed. Please try again.")
                logging.error(f"Failed withdrawal to {recipient_address}")
        except Exception as e:
            logging.error(f"Unexpected withdrawal error: {e}")

    def track_transactions(self):
        """Listen for incoming BTC transactions via WebSocket with error handling."""
        while True:
            try:
                def on_message(ws, message):
                    data = json.loads(message)
                    if "x" in data:
                        for output in data["x"]["out"]:
                            if output["addr"] == self.deposit_address:
                                received_btc = output["value"] / SATOSHIS_PER_BTC
                                self.balance += received_btc
                                self.balance_label.config(text=f"Balance: {self.balance:.8f} BTC")
                                self.result_label.config(text=f"Received {received_btc:.8f} BTC!")
                                self.higher_button.config(state=tk.NORMAL)
                                self.lower_button.config(state=tk.NORMAL)
                                message = f"Received deposit: {received_btc:.8f} BTC"
                                self.update_transaction_history(message)

                def on_open(ws):
                    ws.send(json.dumps({"op": "addr_sub", "addr": self.deposit_address}))

                ws = websocket.WebSocketApp(WS_URL, on_message=on_message, on_open=on_open)
                ws.run_forever()

            except Exception as e:
                logging.error(f"Unexpected WebSocket error: {e}")
                time.sleep(10)

# Initialize GUI
root = tk.Tk()
game = HighLowGameGUI(root)
logging.info("Starting GUI...")
root.mainloop()
