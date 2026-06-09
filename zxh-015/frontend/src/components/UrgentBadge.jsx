export default function UrgentBadge({ reason }) {
  return (
    <span className="inline-flex items-center gap-1 text-xs bg-red-100 text-red-600 px-2 py-0.5 rounded-full animate-pulse">
      <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
      紧急
      {reason && <span className="text-red-400">- {reason}</span>}
    </span>
  )
}
