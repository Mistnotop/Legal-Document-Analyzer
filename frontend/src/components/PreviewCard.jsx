import { HiOutlineDocumentText } from "react-icons/hi";

function PreviewCard({ preview }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center gap-3">
        <div className="grid size-9 place-items-center rounded-md bg-indigo-50 text-indigo-700">
          <HiOutlineDocumentText className="size-5" />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-slate-950">Document Preview</h2>
          <p className="text-sm text-slate-500">Extracted or pasted text sample</p>
        </div>
      </div>

      <div className="min-h-36 rounded-md border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-700">
        {preview ? (
          <p className="whitespace-pre-wrap break-words">{preview}</p>
        ) : (
          <p className="text-slate-400">No document preview yet.</p>
        )}
      </div>
    </section>
  );
}

export default PreviewCard;
