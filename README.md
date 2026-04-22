# 📸 PDF Photo Extractor

A simple and powerful Streamlit app to extract all photos from a PDF file as separate images — with no quality loss.

---

## 🚀 Features

* Extracts **only embedded images** (ignores text)
* Saves each photo as a **separate file**
* Removes **duplicate images**
* Filters out **small icons/logos**
* Shows **preview thumbnails**
* Download all images as a **ZIP file**
* Works smoothly with **200+ images**

---

## 🛠️ Tech Stack

* Python
* Streamlit
* PyMuPDF (fitz)

---

## 📂 Project Structure

```
pdf-photo-extractor/
│── app.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation (Run Locally)

### 1. Clone the repository

```
git clone https://github.com/ops523/Extract-Photos-From-PDF.git
cd Extract-Photos-From-PDF
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the app

```
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to https://share.streamlit.io
3. Click **New App**
4. Select your repository
5. Set main file path: `app.py`
6. Click **Deploy**

---

## 📦 How It Works

* The app reads the PDF using PyMuPDF
* Extracts all embedded image objects
* Filters based on size to remove noise
* Packages images into a ZIP file
* Provides preview + download

---

## ⚠️ Limitations

* If the PDF is **scanned (image-based)**:

  * Images may not be extracted individually
  * Entire pages may behave as single images

---

## 🔧 Configuration

You can adjust:

* **Minimum Image Size Filter**
  Helps remove small unwanted elements like logos/icons

---

## 💡 Future Improvements

* Bulk PDF upload
* AI-based image classification (receipts, handwritten, etc.)
* Google Drive integration
* Auto-renaming based on content

---

## 🤝 Contributing

Feel free to fork the repo and submit pull requests.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 🙌 Acknowledgements

* Streamlit
* PyMuPDF

---

## 📬 Contact

For any questions or improvements, feel free to reach out.

---
