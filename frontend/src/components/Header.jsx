import { HiOutlineDocumentSearch } from "react-icons/hi";

function Header() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="grid size-10 place-items-center rounded-lg bg-slate-900 text-white">
            <HiOutlineDocumentSearch className="size-6" />
          </div>
          <div>
            <h1 className="text-xl font-semibold tracking-normal text-slate-950">
              Legal Document Analyzer
            </h1>
            <p className="text-sm text-slate-500">AI contract classification</p>
          </div>
        </div>

        <span className="rounded-md border border-emerald-200 bg-emerald-50 px-3 py-1 text-sm font-medium text-emerald-700">
          Model Ready
        </span>
      </div>
    </header>
  );
}

export default Header;
