# Algorithm Performance Evaluator 🚀

## 📖 Project Overview
The **Algorithm Performance Evaluator** is a comprehensive desktop application designed to bridge the gap between theoretical Big O analysis and practical algorithm execution[cite: 2]. It empowers users to write custom algorithms, evaluate their runtime against varying input sizes, and automatically estimate their time complexity with high precision[cite: 2]. 

This project was developed for the **Algorithms (CSE 2nd Year)** course at the Computer and Systems Engineering department (Academic Year: 2025/2026)[cite: 2].

## 🛠️ Tech Stack
*   **Language:** Python[cite: 2]
*   **GUI Framework:** CustomTkinter (for a modern, decoupled UI)[cite: 2]
*   **Data Visualization:** Matplotlib[cite: 2]
*   **Core Systems:** `multiprocessing` (for true concurrency) and `sys` (for memory/stack tracking)[cite: 2]

## 🏗️ Architectural Highlights
Built with a rigorous engineering mindset, the application features:
*   **Decoupled Architecture:** The Graphical User Interface (GUI) is strictly separated from the execution and mathematical analysis backend[cite: 2]. Communication is handled seamlessly via callbacks to prevent UI freezing during heavy, CPU-bound computations[cite: 2].
*   **Custom AST/Trace Debugger:** The Manual Mode is powered by a custom-built mini-debugger utilizing the `sys.settrace` module[cite: 2]. It actively captures stack frames and local variables at runtime, allowing users to visualize the control flow step-by-step without altering their source code[cite: 2].
*   **Static Analyzer:** Predicts Big O notation by detecting loops and method calls within the algorithm's structure[cite: 2].

## ⚙️ Operational Modes
1.  **Auto Mode:** Automatically generates random inputs of varying sizes and measures execution time across multiple scenarios (sorted, reversed, and random cases)[cite: 2]. It then applies advanced mathematical curve fitting to pinpoint the closest Big O complexity class[cite: 2].
2.  **Manual Mode:** Acts as an interactive debugging environment[cite: 2]. Users can input a specific, custom array manually and track the algorithm's execution step-by-step to verify logic and isolate edge cases[cite: 2].

## 📊 Supported Time Complexities
The estimation engine successfully detects and plots the following complexity classes:
*   $O(1)$ - Constant Time (e.g., Array Index Access)[cite: 2]
*   $O(n)$ - Linear Time (e.g., Linear Search)[cite: 2]
*   $O(n \log n)$ - Linearithmic Time (e.g., Merge Sort)[cite: 2]
*   $O(n^2)$ - Quadratic Time (e.g., Insertion Sort)[cite: 2]
*   $O(n^3)$ - Cubic Time cite: [cite: 2]
*   $O(2^n)$ - Exponential Time (e.g., Recursive Fibonacci)[cite: 2]
*   $O(n!)$ - Factorial Time[cite: 2]

## 👨‍💻 Team Contribution
**Note:** This project was developed as a solo full-stack engineering effort[cite: 2]. All architectural, logical, and interface components were designed and implemented by a single developer[cite: 2].

| Developer | Role & Contribution |
| :--- | :--- |
| **Othman Mohamed Salem Ibrahim** | Full System Architecture, Multiprocessing Engine, Custom Debugger, GUI Design, Mathematical Analysis & Documentation[cite: 2]. |

---
*Supervised by Dr. Hend Gaballah & Eng. Mahmoud Ibrahim*[cite: 2]
