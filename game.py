import cv2
import mediapipe as mp
import streamlit as st
import numpy as np
import time
import random

# Initialize Mediapipe hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Game settings
FRAME_WIDTH, FRAME_HEIGHT = 640, 480
BALL_COUNT = 3
BALL_LIFETIME = 5  # seconds
GAME_DURATION = 60  # seconds
BALL_COLORS = [(0, 255, 0), (0, 165, 255), (0, 0, 255)]  # Green, Orange, Red
BALL_POINTS = [1, 2, 3]

def generate_ball():
    return {
        "x": random.randint(50, FRAME_WIDTH - 50),
        "y": random.randint(50, FRAME_HEIGHT - 50),
        "color": random.choice(BALL_COLORS),
        "points": BALL_POINTS[BALL_COLORS.index(random.choice(BALL_COLORS))],
        "spawn_time": time.time()
    }

def main():
    st.title("Gesture-Controlled Snake Game")
    
    with st.sidebar:
        start_button = st.button("Start Game")
        score_placeholder = st.empty()
        time_placeholder = st.empty()
        restart_button = st.button("Restart Game")
    
    if not start_button:
        st.stop()
    
    cap = cv2.VideoCapture(0)
    cap.set(3, FRAME_WIDTH)
    cap.set(4, FRAME_HEIGHT)
    
    score = 0
    start_time = time.time()
    balls = [generate_ball() for _ in range(BALL_COUNT)]
    snake_trail = []
    
    # Streamlit image placeholder
    image_placeholder = st.empty()
    
    while time.time() - start_time < GAME_DURATION:
        success, frame = cap.read()
        if not success:
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger = hand_landmarks.landmark[8]
                x, y = int(index_finger.x * FRAME_WIDTH), int(index_finger.y * FRAME_HEIGHT)
                snake_trail.append((x, y))
                if len(snake_trail) > 20:
                    snake_trail.pop(0)
                
                for ball in balls:
                    if abs(x - ball["x"]) < 20 and abs(y - ball["y"]) < 20:
                        score += ball["points"]
                        balls.remove(ball)
                        balls.append(generate_ball())
                
                for i in range(len(snake_trail) - 1):
                    cv2.line(frame, snake_trail[i], snake_trail[i + 1], (0, 255, 0), 5)  # Green and thicker
        
        current_time = time.time()
        balls = [ball for ball in balls if current_time - ball["spawn_time"] < BALL_LIFETIME]
        while len(balls) < BALL_COUNT:
            balls.append(generate_ball())
        
        for ball in balls:
            cv2.circle(frame, (ball["x"], ball["y"]), 15, ball["color"], -1)
            cv2.putText(frame, str(ball["points"]), (ball["x"] - 5, ball["y"] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        # Update sidebar with score and time
        score_placeholder.write(f"### Score: {score}")
        time_placeholder.write(f"### Time Left: {int(GAME_DURATION - (current_time - start_time))}s")
        
        # Update the same image container instead of printing new frames
        image_placeholder.image(frame, channels="BGR")
    
    cap.release()
    st.sidebar.write(f"### Game Over! Your Score: {score}")
    
if __name__ == "__main__":
    main()
