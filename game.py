import cv2
import mediapipe as mp
import streamlit as st
import time
import random
from collections import deque

# Mediapipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,  # Lower for faster start
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils  

# Game settings
FRAME_WIDTH, FRAME_HEIGHT = 640, 480
BALL_COUNT = 3
BALL_LIFETIME = 5  
GAME_DURATION = 60  
BALL_COLORS = [(0, 255, 0), (0, 165, 255), (0, 0, 255)]
BALL_POINTS = [1, 2, 3]

def generate_ball():
    """Generate a new ball at a random position with random points and color."""
    color_idx = random.randint(0, len(BALL_COLORS) - 1)
    return {
        "x": random.randint(50, FRAME_WIDTH - 50),
        "y": random.randint(50, FRAME_HEIGHT - 50),
        "color": BALL_COLORS[color_idx],
        "points": BALL_POINTS[color_idx],
        "spawn_time": time.time()
    }

# Initialize game variables
if "game_running" not in st.session_state:
    st.session_state.game_running = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "balls" not in st.session_state:
    st.session_state.balls = [generate_ball() for _ in range(BALL_COUNT)]
if "snake_trail" not in st.session_state:
    st.session_state.snake_trail = deque(maxlen=15)

# Pre-initialize the camera for a faster start
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_WIDTH)
cap.set(4, FRAME_HEIGHT)

st.title("Gesture-Controlled Snake Game")

col1, col2 = st.columns(2)
score_box = col1.empty()
time_box = col2.empty()

# Start button
if not st.session_state.game_running:
    if st.button("Start Game"):
        st.session_state.game_running = True
        st.session_state.score = 0
        st.session_state.balls = [generate_ball() for _ in range(BALL_COUNT)]
        st.session_state.snake_trail.clear()
        st.session_state.start_time = time.time()  # Start immediately
    st.stop()

image_placeholder = st.empty()

while st.session_state.game_running:
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    current_time = time.time()
    time_left = max(0, int(GAME_DURATION - (current_time - st.session_state.start_time)))

    # Hand Tracking
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger = hand_landmarks.landmark[8]
            x, y = int(index_finger.x * FRAME_WIDTH), int(index_finger.y * FRAME_HEIGHT)

            # Update snake trail
            st.session_state.snake_trail.append((x, y))

            # Collision Detection
            for ball in st.session_state.balls:
                if abs(x - ball["x"]) < 20 and abs(y - ball["y"]) < 20:
                    st.session_state.score += ball["points"]
                    st.session_state.balls.remove(ball)
                    st.session_state.balls.append(generate_ball())

            # Draw snake trail
            for i in range(len(st.session_state.snake_trail) - 1):
                cv2.line(frame, st.session_state.snake_trail[i], st.session_state.snake_trail[i + 1], (0, 255, 0), 5)

    # Remove old balls
    st.session_state.balls = [ball for ball in st.session_state.balls if current_time - ball["spawn_time"] < BALL_LIFETIME]
    while len(st.session_state.balls) < BALL_COUNT:
        st.session_state.balls.append(generate_ball())

    # Draw balls
    for ball in st.session_state.balls:
        cv2.circle(frame, (ball["x"], ball["y"]), 15, ball["color"], -1)
        cv2.putText(frame, str(ball["points"]), (ball["x"] - 5, ball["y"] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Update UI
    score_box.markdown(f"### Score: {st.session_state.score}")
    time_box.markdown(f"### Time Left: {time_left}s")

    image_placeholder.image(frame, channels="BGR")

    if time_left <= 0:
        st.session_state.game_running = False

cap.release()

# Show Game Over Screen
st.markdown(f"## Game Over! 🎮 Your Score: {st.session_state.score}")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Restart Game"):
        st.session_state.game_running = True
        st.session_state.start_time = None
        st.session_state.score = 0
        st.session_state.balls = [generate_ball() for _ in range(BALL_COUNT)]
        st.session_state.snake_trail.clear()
        st.rerun()
with col2:
    if st.button("Exit"):
        st.stop()
