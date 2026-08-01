import { HiOutlineCpuChip } from "react-icons/hi2";

const classes = [
  { label: "credit_loan", description: "Credit & Loan Agreements" },
  { label: "employment", description: "Employment Agreements" },
  { label: "lease", description: "Lease & Rental Agreements" },
  { label: "license_ip", description: "IP & Licensing Agreements" },
  {
    label: "merger_acquisition",
    description: "Mergers & Acquisitions Agreements",
  },
  { label: "purchase_sale", description: "Purchase & Sale Agreements" },
  { label: "service_supply", description: "Service & Supply Contracts" },
  {
    label: "settlement_release",
    description: "Settlement & Release Agreements",
  },
  {
    label: "shareholder_rights",
    description: "Shareholder Rights & Governance",
  },
];

function formatLabel(label) {
  return label
    .replace(/&/g, " & ")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function ModelInfoCard() {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center gap-3">
        <div className="grid size-9 place-items-center rounded-md bg-violet-50 text-violet-700">
          <HiOutlineCpuChip className="size-5" />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-slate-950">Model Information</h2>
          <p className="text-sm text-slate-500">Current classifier configuration</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
          <p className="text-slate-500">Model</p>
          <p className="mt-1 font-semibold text-slate-950">LinearSVC</p>
        </div>
        <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
          <p className="text-slate-500">Features</p>
          <p className="mt-1 font-semibold text-slate-950">TF-IDF</p>
        </div>
        <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
          <p className="text-slate-500">Classes</p>
          <p className="mt-1 font-semibold text-slate-950">9 document classes</p>
        </div>
        <div className="rounded-md border border-slate-200 bg-slate-50 p-3">
          <p className="text-slate-500">Test Accuracy</p>
          <p className="mt-1 font-semibold text-slate-950">92.81%</p>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {classes.map(({ label, description }) => (
          <span
            key={label}
            title={description}
            className="rounded-md border border-slate-200 bg-white px-2.5 py-1 text-xs font-medium text-slate-600"
          >
            {formatLabel(label)}
          </span>
        ))}
      </div>
    </section>
  );
}

export default ModelInfoCard;
