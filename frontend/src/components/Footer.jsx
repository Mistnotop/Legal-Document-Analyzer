function Footer() {
  const githubUrl = import.meta.env.VITE_GITHUB_URL || "https://github.com/";

  return (
    <footer className="border-t border-slate-200 bg-white">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-3 px-4 py-5 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
        <p>
          <span className="font-semibold text-slate-800">Legal Document Analyzer</span>{" "}
          by NyaySetu
        </p>
        <p>React, Vite, Tailwind CSS, FastAPI, scikit-learn</p>
        <a
          className="font-medium text-cyan-700 hover:text-cyan-800"
          href={githubUrl}
          target="_blank"
          rel="noreferrer"
        >
          GitHub
        </a>
      </div>
    </footer>
  );
}

export default Footer;
