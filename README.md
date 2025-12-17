# 👁️ EyeNav – Hands-Free Screen Control System

> Control your computer using only your eyes 👀  
> A real-time, vision-based accessibility system for hands-free screen interaction.

---

## 🌟 Project Overview

**EyeNav** is a computer vision–based assistive technology that allows users to control their computer without a mouse, keyboard, or touchpad.  
Using eye movement and blink gestures, the system enables natural and intuitive interaction with the screen.

This project focuses on **accessibility, human–computer interaction, and real-time eye tracking**.

---

## 🚀 Features

- 👁️ Eye-based cursor movement  
- 🖱️ Single blink → Left click  
- 📦 Long blink → Drag & Drop  
- 📜 Look up / down → Scroll  
- ⏸️ Eyes closed for 3 seconds → Pause / Resume  
- 🎯 Smooth & stable cursor movement  
- ⚡ Real-time performance on macOS  

---

## 🧠 How It Works

1. Webcam captures live video frames  
2. Face and eye landmarks are detected using MediaPipe Face Mesh  
3. Iris movement controls the mouse cursor  
4. Blink duration determines click or drag actions  
5. Cursor smoothing reduces jitter  
6. Eye direction controls scrolling behavior  

---

## 🛠️ Tech Stack

- Python 3.11  
- OpenCV  
- MediaPipe Face Mesh  
- PyAutoGUI  
- NumPy  
- macOS Accessibility APIs  

---

## 💻 System Requirements

- macOS 12 or later  
- Python 3.11  
- Webcam (built-in or external)  
- Good lighting conditions  

---

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/eyenav.git
cd eyenav
