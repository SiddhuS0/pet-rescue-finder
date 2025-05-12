# 🐾 Pet Rescue Finder

**Pet Rescue Finder** is a machine learning-powered web application that helps users report, find, and adopt lost or abandoned pets using image recognition and geolocation features. It notifies nearby rescue centers and allows pet owners to search for matches based on photo + feature similarity.

## 🚀 Features

- 📷 Upload photos of found or lost pets
- 📍 Auto-fetch and use geolocation (latitude & longitude)
- 🧠 ML-powered description generator (color, breed, size)
- 🧭 Notify nearby rescue centers based on location
- 🔍 Search for lost pets using combined image and metadata matching
- ❤️ Mark pets as rescued or available for adoption
- 📝 Register volunteers with location info

## 🛠 Tech Stack

### Frontend:
- Streamlit (UI)
- `streamlit_js_eval` (for geolocation)
- Lottie animations for UI enhancement

### Backend:
- FastAPI (API server)
- CLIP-based image model for similarity
- Custom feature-based matching logic
- JSON-based storage for pets and volunteers
- Google Maps API for rescue center location matching

## 📁 Project Structure

```
pet-rescue-finder/
├── frontend/
│   └── app.py
├── backend/
│   ├── routes.py
│   ├── utils/
│   │   └── matching.py, geolocation.py
├── data/
│   └── pets.json, volunteers.json, rescue_centers.json
├── requirements.txt
├── README.md
```

## ⚙️ Installation & Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/SiddhuS0/pet-rescue-finder.git
cd pet-rescue-finder
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the backend (FastAPI)

```bash
cd backend
uvicorn routes:app --reload --port 8000
```

### 5. Run the frontend (Streamlit)

```bash
cd ../frontend
streamlit run app.py
```

## 🌐 Deployment

- **Frontend**: Deployed on Streamlit Cloud
- **Backend**: Deployed on Render

To deploy on Render:
1. Set `Root Directory` as `backend`
2. Set Start Command:  
   ```bash
   uvicorn routes:app --host 0.0.0.0 --port 10000
   ```

## 📦 API Endpoints (FastAPI)

- `POST /upload_pet` – Upload pet with image & location
- `POST /search_pet` – Search pet using image + features
- `POST /register_volunteer` – Register a volunteer
- `GET /rescue_centers` – Get nearby rescue centers

## 🤝 Contributing

Feel free to fork the repo and submit a PR. Contributions to:
- UI/UX improvements
- More accurate ML models
- Feature suggestions

are always welcome!

## 🧑‍💻 Author

Made with ❤️ by TEAM AURA
[Siddhartha Yenumula](https://github.com/SiddhuS0)
[Ashish Sai Vardhan Karingula](https://github.com/ashishsai-2611)
[Sri Ram Neerukonda](https://github.com/NSriram27)
[Pavan Kalyan Paidipelli](https://github.com/pavan123kalyan)


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
