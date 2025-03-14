# Gesture Controlled Snake Game - README

## 📌 Introduction
Play the classic **Snake game** using just your hand gestures! This game uses **OpenCV** and **MediaPipe** to track hand movements via a webcam, allowing you to guide the snake and collect points.

## ✨ Features
- **Hand-Controlled Snake:** Move your hand to navigate the snake.
- **Smooth Movement & Trails** for a better gaming experience.
- **Real-time Score & Timer** displayed on the sidebar.
- **Dynamic Ball Mechanics:**
  - **3 Balls Always on Screen:** New balls appear when one is collected or expires.
  - **Point System:**
    - 🟢 Green Ball → 1 Point  
    - 🟠 Orange Ball → 2 Points  
    - 🔴 Red Ball → 3 Points  
- **Ball Collection System:**
  - If the snake touches a ball, it disappears and adds points to the score.
  - If the ball is not collected in **5 seconds**, it disappears and a new one appears.
- **Game Over Screen** with the final score displayed and an automatic restart after timeout.
- **Sound effects** when collecting balls.
- **OpenCV Game Window Embedded in Streamlit.**

## 🎮 How to Play?
1️⃣ **Run the game:**  
```sh
streamlit run GestureSnakeGame.py
```
2️⃣ **Start the game** by clicking **"Start Game"** in the sidebar.  
3️⃣ **Control the Snake with Your Hand:** Move your hand in front of the camera to navigate the snake.  
4️⃣ **Collect the balls** (🟢🟠🔴) to gain points.  
5️⃣ The game lasts **60 seconds**, after which a **Game Over** screen appears with your final score.

## 🏗️ Technologies Used
- **Python**
- **OpenCV** (for real-time video processing)
- **MediaPipe** (for hand tracking)
- **Streamlit** (for embedding the OpenCV window in a web-based UI)

## 🛠️ Setup & Installation
1️⃣ **Clone the repository:**
```sh
  git clone https://github.com/MehnazAli2004/PennyWise.git
  cd PennyWise
```

2️⃣ **Install dependencies:**
```sh
pip install -r requirements.txt
```

3️⃣ **Run the game:**
```sh
streamlit run GestureSnakeGame.py
```

4️⃣ **Grant camera access** when prompted and start playing!

## 🚀 Future Enhancements
- 🟡 **Collision Detection** (self-collision & walls)
- 🟡 **Leaderboard & High Scores**
- 🟡 **Power-ups & Special Abilities**
- 🟡 **Multiplayer Mode**
- 🟡 **Improved Graphics & UI Enhancements**

## 📜 License
This project is open-source. Feel free to use, modify, and contribute!
