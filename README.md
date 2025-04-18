High or Low BTC Game – Educational Edition
Purpose
This program was designed as an educational tool to introduce young students, aspiring hobbyists, and beginners to real-world programming concepts using Python. It teaches fundamentals such as variables, functions, randomization, GUI development, API integration, and blockchain technology in a fun, interactive way.
Students can learn how Bitcoin transactions work by generating deposit addresses, tracking deposits in real-time using WebSocket API, and even withdrawing winnings to their own BTC wallets.

Features
✔ Interactive High/Low Bitcoin Betting Game
✔ Real-Time BTC Deposits via Blockchain API
✔ Live WebSocket Tracking for Incoming Transactions
✔ Secure Withdrawals to Player Wallets
✔ Transaction History Panel for Tracking Deposits & Bets
✔ Error Handling & Logging to Ensure Stability

How the Program Was Developed and Tested
1️⃣ GUI Interface – Tkinter Framework
- The program was built using Python’s Tkinter library to create a simple, interactive interface.
- We tested window sizing, button states, and balance updates to ensure smooth gameplay.
- To prevent resizing issues, balance text was enclosed in a frame.
2️⃣ Randomized Gameplay Mechanics
- We used Python's random module to generate numbers between 0 and 100, determining win/loss conditions.
- We tested different betting amounts and incorrect inputs to ensure proper error handling.
3️⃣ Bitcoin Address Generation
- The program connects to the Blockchain.com API to generate BTC deposit addresses dynamically.
- Testing involved verifying address creation, ensuring API calls returned correct responses.
- If the API failed, a fallback error message was introduced to prevent crashes.
4️⃣ WebSocket Real-Time Transaction Tracking
- The WebSocket API (wss://ws.blockchain.info/inv) listens for new BTC deposits.
- Extensive testing ensured that incoming funds automatically update the balance.
- If the WebSocket disconnects, automatic reconnection logic was added to retry every 10 seconds.
5️⃣ Withdrawal System
- Players can withdraw BTC winnings by entering their wallet address.
- The API processes transactions, deducting funds from the in-game balance.
- We tested invalid withdrawals (like exceeding balance) to prevent unauthorized transactions.
6️⃣ Transaction History Panel
- We introduced a scrollable text box to record deposits, bets, and withdrawals for review.
- Entries are logged both visually in the game and in a game.log file for debugging.
- Each transaction updates instantly when a deposit or withdrawal occurs.
7️⃣ Error Handling & Logging
- Comprehensive error handling prevents the program from crashing due to API issues.
- If the WebSocket or API fails, users see a message instead of an abrupt closure.
- Logging (game.log) captures all transactions and errors for debugging.

Future Improvements
🔹 Leaderboard System – Track players with highest BTC winnings.
🔹 Multiplayer Mode – Compete with others in a Bitcoin-powered game session.
🔹 Mobile Compatibility – Convert the interface to work on tablets or phones.

Setup Instructions
🔧 Requirements
- Python 3.7+
- Tkinter (pip install tk)
- WebSocket Client (pip install websocket-client)
- Blockchain API Key (Sign up at Blockchain.com)
💻 Running the Program
1️⃣ Install Python and dependencies (pip install websocket-client).
2️⃣ Get a Blockchain API key and insert it into the script.
3️⃣ Run the program using:
python game.py


4️⃣ Deposit BTC using the generated address and start playing! 🎮

Conclusion
This project was designed to educate students and hobbyists about Python, blockchain technology, and GUI programming in a hands-on, interactive way. We hope this inspires future developers to explore both programming and cryptocurrency mechanics while having fun!
Feel free to contribute, improve, and expand this project! 🚀

Designed alongside CoPilot AI. If you ask where the won bitcoin comes from..... hahahaha..... better be able to pay people out if you implement this code ;-P I built this because I hurt my foot and wanted to play around with API calls based on websockets.
