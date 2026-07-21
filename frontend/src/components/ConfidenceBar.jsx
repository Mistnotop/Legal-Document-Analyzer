function ConfidenceBar({ label, confidence }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between gap-3 text-sm">
        <span className="min-w-0 truncate font-medium text-slate-700">{label}</span>
        <span className="shrink-0 font-semibold text-slate-900">{confidence}%</span>
      </div>
      <div className="h-3 overflow-hidden rounded-sm bg-slate-200">
        <div
          className="h-full rounded-sm bg-cyan-600"
          style={{ width: `${Math.max(2, Math.min(confidence, 100))}%` }}
        />
      </div>
    </div>
  );
}

export default ConfidenceBar;
