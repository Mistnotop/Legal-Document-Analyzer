import { HiOutlineChartBar } from "react-icons/hi";

import ConfidenceBar from "./ConfidenceBar.jsx";

function formatLabel(label) {
  return label
    ? label
        .replace(/&/g, " & ")
        .replace(/_/g, " ")
        .replace(/\b\w/g, (char) => char.toUpperCase())
    : "Awaiting Document";
}

function PredictionCard({ result, isAnalyzing }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-5 flex items-center gap-3">
        <div className="grid size-9 place-items-center rounded-md bg-cyan-50 text-cyan-700">
          <HiOutlineChartBar className="size-5" />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-slate-950">Prediction</h2>
          <p className="text-sm text-slate-500">Model classification result</p>
        </div>
      </div>

      {isAnalyzing ? (
        <div className="space-y-3">
          <div className="h-7 w-3/4 animate-pulse rounded bg-slate-200" />
          <div className="h-4 w-1/2 animate-pulse rounded bg-slate-200" />
          <div className="h-24 animate-pulse rounded bg-slate-100" />
        </div>
      ) : result ? (
        <div className="space-y-6">
          <div className="rounded-md border border-slate-200 bg-slate-50 p-4">
            <p className="text-sm font-medium text-slate-500">Predicted Class</p>
            <p className="mt-1 text-2xl font-semibold text-slate-950">
              {formatLabel(result.predicted_class)}
            </p>
            <p className="mt-2 text-sm text-slate-600">
              Confidence:{" "}
              <span className="font-semibold text-slate-950">
                {result.confidence}%
              </span>
            </p>
          </div>

          <div>
            <h3 className="mb-4 text-sm font-semibold uppercase text-slate-500">
              Top Predictions
            </h3>
            <div className="space-y-4">
              {result.top_predictions?.map((item) => (
                <ConfidenceBar
                  key={item.label}
                  label={formatLabel(item.label)}
                  confidence={item.confidence}
                />
              ))}
            </div>
          </div>
        </div>
      ) : (
        <div className="rounded-md border border-dashed border-slate-300 bg-slate-50 p-6 text-sm text-slate-500">
          Prediction details will appear after analysis.
        </div>
      )}
    </section>
  );
}

export default PredictionCard;
