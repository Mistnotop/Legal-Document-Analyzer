import { useMemo, useState } from "react";

import Footer from "./components/Footer.jsx";
import Header from "./components/Header.jsx";
import ModelInfoCard from "./components/ModelInfoCard.jsx";
import PredictionCard from "./components/PredictionCard.jsx";
import PreviewCard from "./components/PreviewCard.jsx";
import UploadCard from "./components/UploadCard.jsx";
import { predictDocument, predictText } from "./services/api.js";

const MAX_FILE_SIZE = 10 * 1024 * 1024;
const ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"];

function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [preview, setPreview] = useState("");
  const [error, setError] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const canAnalyze = useMemo(() => {
    return Boolean(file || text.trim());
  }, [file, text]);

  function validateFile(selectedFile) {
    const extension = selectedFile.name
      .slice(selectedFile.name.lastIndexOf("."))
      .toLowerCase();

    if (!ALLOWED_EXTENSIONS.includes(extension)) {
      return "Unsupported file type. Please upload a PDF, DOCX, or TXT file.";
    }

    if (selectedFile.size > MAX_FILE_SIZE) {
      return "File is too large. Maximum upload size is 10 MB.";
    }

    return "";
  }

  function handleFileChange(selectedFile, validationMessage = "") {
    setError("");
    setResult(null);
    setPreview("");

    if (validationMessage) {
      setFile(null);
      setError(validationMessage);
      return;
    }

    if (!selectedFile) {
      setFile(null);
      return;
    }

    const validationError = validateFile(selectedFile);

    if (validationError) {
      setFile(null);
      setError(validationError);
      return;
    }

    setFile(selectedFile);
  }

  async function handleAnalyze() {
    if (!canAnalyze || isAnalyzing) {
      return;
    }

    setError("");
    setResult(null);
    setUploadProgress(file ? 5 : 0);
    setIsAnalyzing(true);

    try {
      if (file) {
        const response = await predictDocument(file, (event) => {
          if (!event.total) {
            return;
          }

          setUploadProgress(Math.round((event.loaded * 100) / event.total));
        });
        setResult(response);
        setPreview(response.preview || "");
      } else {
        if (!text.trim()) {
          throw new Error("Document text is empty.");
        }

        const response = await predictText(text);
        setResult(response);
        setPreview(text);
      }
    } catch (apiError) {
      const detail = apiError.response?.data?.detail;
      const offline = apiError.code === "ERR_NETWORK" || !apiError.response;

      setError(
        offline
          ? "Backend is offline. Start the FastAPI server and try again."
          : detail || apiError.message || "Unable to analyze this document."
      );
    } finally {
      setUploadProgress(0);
      setIsAnalyzing(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-100 text-slate-950">
      <Header />

      <section className="mx-auto grid w-full max-w-6xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[1.15fr_0.85fr] lg:px-8">
        <div className="space-y-6">
          <UploadCard
            file={file}
            text={text}
            error={error}
            isAnalyzing={isAnalyzing}
            uploadProgress={uploadProgress}
            canAnalyze={canAnalyze}
            onAnalyze={handleAnalyze}
            onFileChange={handleFileChange}
            onTextChange={setText}
          />
          <PreviewCard preview={preview} />
        </div>

        <div className="space-y-6">
          <PredictionCard result={result} isAnalyzing={isAnalyzing} />
          <ModelInfoCard />
        </div>
      </section>

      <Footer />
    </main>
  );
}

export default App;
