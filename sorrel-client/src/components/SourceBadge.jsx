export default function SourceBadge({ source }) {
    return (
        <div className="mt-2 mr-2 mb-2 inline-flex items-center rounded-md border border-zinc-700/80 bg-zinc-800/40 px-2.5 py-1 text-xs text-zinc-400">
            <span className="text-red-500 font-medium mr-1.5">📄 {source.source_file}</span>
            {source.section_heading && <span className="text-zinc-400">› {source.section_heading}</span>}
            {source.page_number && <span className="text-zinc-500 ml-1.5">(p. {source.page_number})</span>}
        </div>
    );
}