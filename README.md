
```md
```
# AI Homework Assistant 📚🤖  

A Python-based assistant for teachers that **automates homework creation** using AI.  
It generates **personalized homework assignments** for students, stores them in a database, and exports them as PDFs.

---

## 🚀 Features  
- ✅ **Student Management** – Add, update, and retrieve student records.  
- ✅ **Lesson Tracking** – Store lessons and link them to students.  
- ✅ **AI-Powered Homework Generation** – Uses an algorithm to create tailored assignments.  
- ✅ **PDF Export** – Generates a PDF for each student’s homework and saves it in a structured directory.  
- ✅ **Database Integration** – Uses SQLite for storing students, lessons, and homework.

---

## ⚡ Technologies Used  
- **Python** 🐍  
- **SQLite** 🗄️  
- **ReportLab** (for PDF generation) 📄  
- **Object-Oriented Programming (OOP)** 💡  
- **Git & GitHub** 🔗  

---

## 📂 Folder Structure  
```bash
AI-Homework-Assistant/
│── database_manager.py      # Handles database operations  
│── homework_generator.py    # AI-generated homework logic  
│── pdf_generator.py         # Generates PDFs for homework  
│── main.py                  # Main application logic  
│── README.md                # Documentation  
│── requirements.txt         # Required dependencies  
│── data/                    # SQLite database and saved student data  
│── homework_pdfs/           # Generated homework PDFs, organized by student  
```

---

## 📥 Installation Guide  

### 🔹 **1. Clone the Repository**  
```bash
git clone https://github.com/yourusername/AI-Homework-Assistant.git
cd AI-Homework-Assistant
```

### 🔹 **2. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### 🔹 **3. Run the Application**  
```bash
python main.py
```

---

## 📖 How It Works  

1️⃣ **Teacher enters student & lesson details** 📋  
2️⃣ **AI generates a customized homework assignment** 🧠  
3️⃣ **The system stores the homework in the database** 🗄️  
4️⃣ **A PDF is created and saved in the student’s folder** 📄  
5️⃣ **Teacher can access and print assignments anytime** 🖨️  

---

## 🔥 Example Usage  
```bash
Für welchen Schüler (ID)? 1
Für welche Lesson (ID)? 3
✅ Homework (ID: 101) for Max created.
✅ PDF saved: homework_pdfs/Max/Maths_2024-03-10_Max.pdf
```

---

## 🤝 Contributing  
Want to improve this project? Follow these steps:  
1. **Fork** the repo 🍴  
2. Create a **new branch** (`git checkout -b feature-xyz`)  
3. **Commit your changes** (`git commit -m "Added feature XYZ"`)  
4. **Push to GitHub** (`git push origin feature-xyz`)  
5. **Create a Pull Request** 🔥  

---

## 📄 License  
This project is licensed under the **MIT License**.

---
```
