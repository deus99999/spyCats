# spyCats

This is a full-stack project consisting of:

- **Backend**: FastAPI-based REST API
- **Frontend**: Next.js React application with App Router

It allows you to manage secret agent cats, their missions, and mission targets.

---

## 🚀 Features

### 🐱 Cats
- List all cats
- View and edit cat salary
- Delete cat

### 🎯 Missions
- Create a mission 
- Assign a cat to a mission
- Update target notes (if not complete)
- Delete missions 

---

## 🛠️ How to Run the Project

### Requirements

- Python 3.10+
- Node.js 18+
- SQLite database
- `pip`, `npm`, or `yarn`

---

### 📦 Backend (FastAPI)

1. **Navigate to the backend folder:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

uvicorn main:app --reload 
```

### 📦 Frontend (Next.js React)

1. **Navigate to the frontend folder:**

```bash
cd frontend
```

2. **Install dependencies:**

```bash
npm install
# or
yarn
```

 3. **Run development server:**

```bash
npm run dev
# or
yarn dev
```
#Visit in browser:

```http://localhost:3000```
