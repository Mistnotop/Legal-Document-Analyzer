import { useDropzone } from "react-dropzone";
import {
  HiOutlineCloudArrowUp,
  HiOutlineDocument,
  HiOutlinePlay,
  HiOutlineXMark,
} from "react-icons/hi2";

import LoadingSpinner from "./LoadingSpinner.jsx";

function UploadCard({
  file,
  text,
  error,
  isAnalyzing,
  uploadProgress,
  canAnalyze,
  onAnalyze,
  onFileChange,
  onTextChange,
}) {
  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    multiple: false,
    maxSize: 10 * 1024 * 1024,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
        ".docx",
      ],
      "text/plain": [".txt"],
    },
    onDrop: (acceptedFiles) => {
      onFileChange(acceptedFiles[0] || null);
    },
    onDropRejected: () => {
      onFileChange(
        null,
        "Unsupported file or file too large. Upload a PDF, DOCX, or TXT file under 10 MB."
      );
    },
  });

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-5">
        <h2 className="text-lg font-semibold text-slate-950">
          Upload PDF / DOCX / TXT
        </h2>
        <p className="text-sm text-slate-500">
          Analyze an uploaded file or paste contract text below.
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`grid min-h-32 cursor-pointer place-items-center rounded-lg border border-dashed p-5 text-center transition ${
          isDragReject
            ? "border-rose-500 bg-rose-50"
            : ""
        } ${
          isDragActive
            ? "border-cyan-500 bg-cyan-50"
            : "border-slate-300 bg-slate-50 hover:border-cyan-500 hover:bg-cyan-50"
        }`}
      >
        <input {...getInputProps()} />
        <div className="space-y-2">
          <HiOutlineCloudArrowUp className="mx-auto size-8 text-cyan-700" />
          <p className="font-medium text-slate-800">
            {isDragReject
              ? "Only PDF, DOCX, or TXT under 10 MB"
              : isDragActive
                ? "Drop the file here"
                : "Choose or drop a document"}
          </p>
          <p className="text-sm text-slate-500">PDF, DOCX, or TXT up to 10 MB</p>
        </div>
      </div>

      {file ? (
        <div className="mt-3 flex items-center justify-between gap-3 rounded-md border border-slate-200 bg-white px-3 py-2">
          <div className="flex min-w-0 items-center gap-2">
            <HiOutlineDocument className="size-5 shrink-0 text-slate-500" />
            <span className="truncate text-sm font-medium text-slate-700">
              {file.name}
            </span>
          </div>
          <button
            type="button"
            className="grid size-8 shrink-0 place-items-center rounded-md text-slate-500 hover:bg-slate-100 hover:text-slate-900"
            onClick={() => onFileChange(null)}
            disabled={isAnalyzing}
            aria-label="Remove selected file"
          >
            <HiOutlineXMark className="size-5" />
          </button>
        </div>
      ) : null}

      <div className="my-5 flex items-center gap-3">
        <div className="h-px flex-1 bg-slate-200" />
        <span className="text-sm font-medium text-slate-400">or</span>
        <div className="h-px flex-1 bg-slate-200" />
      </div>

      <label className="block text-sm font-semibold text-slate-700">
        Paste Document Text
      </label>
      <textarea
        value={text}
        onChange={(event) => onTextChange(event.target.value)}
        disabled={isAnalyzing}
        className="mt-2 min-h-48 w-full resize-y rounded-md border border-slate-300 bg-white p-4 text-sm leading-6 text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-cyan-600 focus:ring-4 focus:ring-cyan-100"
        placeholder="Paste contract clauses or full document text here..."
      />

      {isAnalyzing && file ? (
        <div className="mt-4">
          <div className="mb-2 flex items-center justify-between text-sm">
            <span className="font-medium text-slate-600">Uploading</span>
            <span className="font-semibold text-slate-900">{uploadProgress}%</span>
          </div>
          <div className="h-2 overflow-hidden rounded-sm bg-slate-200">
            <div
              className="h-full bg-cyan-600 transition-all"
              style={{ width: `${Math.max(5, uploadProgress)}%` }}
            />
          </div>
        </div>
      ) : null}

      {error ? (
        <div className="mt-4 rounded-md border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">
          {error}
        </div>
      ) : null}

      <div className="mt-5 flex justify-center">
        <button
          type="button"
          disabled={!canAnalyze || isAnalyzing}
          onClick={onAnalyze}
          className="inline-flex min-h-11 items-center justify-center gap-2 rounded-md bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isAnalyzing ? <LoadingSpinner /> : <HiOutlinePlay className="size-5" />}
          {isAnalyzing ? "Analyzing..." : "Analyze Document"}
        </button>
      </div>
    </section>
  );
}

export default UploadCard;
