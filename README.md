# 🎮 Hand Gesture Gaming Interface

A real-time computer vision project that enables users to control games using hand gestures instead of a keyboard. The system uses a webcam to detect hand movements with MediaPipe and translates gestures into keyboard inputs, providing a touch-free gaming experience.

---

## 📖 Overview

The Hand Gesture Gaming Interface is built using Python, OpenCV, and MediaPipe. It detects hand landmarks in real time, recognizes predefined gestures, and maps them to keyboard controls. The project demonstrates the practical application of computer vision, gesture recognition, and human-computer interaction.

---

## ✨ Features

* 🖐️ Real-time hand gesture recognition
* 📷 Webcam-based input
* 🎮 Control games without a keyboard or mouse
* ⚡ Smooth and responsive gesture detection
* 🔄 Automatic key press and release
* 🖥️ Live gesture visualization
* 💻 Lightweight and easy to run
* 🔧 Easily customizable for other games

---

## 🎯 Gesture Controls

| Hand Gesture        | Action                       |
| ------------------- | ---------------------------- |
| 3 or 4 Fingers Open | Accelerate (Right Arrow Key) |
| 0 or 1 Finger Open  | Brake (Left Arrow Key)       |
| 2 Fingers Open      | Coasting (No Key Pressed)    |
| No Hand Detected    | Release All Keys             |

Press **Q** to exit the application.

---

## 🛠️ Technologies Used

* Python 3.12+
* OpenCV
* MediaPipe
* Pynput

---

## 📂 Project Structure

```text
Hand-Gesture-Gaming-Interface/
│
├── GAME.py
├── README.md
└── .vscode
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hritikkedar19/Hand-Gesture-Gaming-Interface.git
```

### 2. Navigate to the Project Folder

```bash
cd Hand-Gesture-Gaming-Interface
```

### 3. Install Dependencies

```bash

py -3.12 -m pip install mediapipe==0.10.14
```

---

## ▶️ Running the Project

```bash
py -3.12 GAME.py
```

Make sure:
* Version of game
* Your webcam is connected and accessible.
* The target game window is active.
* Good lighting is available for accurate hand detection.

---

## 🔍 How It Works

1. Captures live video from the webcam.
2. Detects hand landmarks using MediaPipe.
3. Counts the number of extended fingers.
4. Maps gestures to keyboard commands.
5. Sends virtual key presses using Pynput.
6. Displays the detected gesture on the screen.

---

## 💡 Applications

* Gesture-controlled gaming
* Computer Vision projects
* Human-Computer Interaction (HCI)
* AI-based input systems
* Educational computer vision demonstrations

---

## 🚀 Future Enhancements

* Multi-hand gesture support
* Custom gesture mapping
* Gesture calibration mode
* Steering control using hand movement
* GUI settings panel
* Support for multiple games
* Performance optimization using GPU acceleration

---

