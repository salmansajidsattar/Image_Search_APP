# 🖼️ Image Search App

An end-to-end **Image Search Application** built with:

- 🔍 **CLIP Model** (OpenAI) for encoding image-text similarity  
- 📦 **Elasticsearch** for indexing and searching  
- 📊 **Kibana** for visualizing the data  
- 🖥️ **Streamlit** for a user-friendly web interface  
- 🐳 **Docker Compose** for managing services  
- 🧠 **Kaggle Dataset** downloaded via Python script  

---

## 🚀 Features

- Upload an image or enter a text query to find similar images  
- Efficient vector search using Elasticsearch  
- Real-time visualization with Streamlit  
- Kibana dashboard for exploring indexed data  
- Automated data ingestion from Kaggle  

---


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/salmansajidsattar/Image_Search_APP/
cd image-search-app
```

## Launch Elasticsearch and Kibana
```bash
cd docker
docker-compose up -d
```

* Elasticsearch: http://localhost:9200

* Kibana: http://localhost:5601

## Download and Preprocess Dataset
```bash
python download_dataset.py
python utils.py
```

## Launch Streamlit UI
```bash
streamlit run main.py
```

## 🖼️ Demo Screenshot

![App Screenshot](https://github.com/salmansajidsattar/Image_Search_APP/blob/main/demo.png)

## 🧠 Model Used

**[CLIP (Contrastive Language–Image Pretraining)](https://github.com/openai/CLIP)** — Trained by OpenAI, allows zero-shot image search by encoding both images and text into the same vector space.

---

## 📸 Dataset

Dataset is automatically downloaded from [Kaggle](https://www.kaggle.com/)

---

## 📊 Kibana Dashboard

Kibana is automatically connected to your Elasticsearch instance.  
You can create index patterns and visualize data after ingestion.

---

## 🛠️ Technologies

- **Python**  
- **Streamlit**  
- **Elasticsearch**  
- **Kibana**  
- **Docker Compose**  
- **CLIP by OpenAI**


