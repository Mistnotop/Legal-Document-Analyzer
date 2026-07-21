import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export async function predictText(text) {
  const response = await api.post("/predict", { text });
  return response.data;
}

export async function predictDocument(file, onUploadProgress) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await api.post("/predict-document", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    onUploadProgress,
  });

  return response.data;
}
