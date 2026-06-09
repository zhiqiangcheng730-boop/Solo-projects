import { useState } from 'react'

export default function ReviewForm({ onSubmit }) {
  const [rating, setRating] = useState(5)
  const [comment, setComment] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit({ rating, comment })
    setRating(5)
    setComment('')
  }

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 rounded-lg p-4">
      <h4 className="font-medium text-gray-700 mb-2">提交评价</h4>
      <div className="flex items-center gap-1 mb-3">
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            key={n}
            type="button"
            onClick={() => setRating(n)}
            className={`text-2xl ${n <= rating ? 'text-yellow-400' : 'text-gray-300'}`}
          >
            ★
          </button>
        ))}
      </div>
      <textarea
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        rows={2}
        className="w-full border border-gray-200 rounded-lg p-2 text-sm mb-2"
        placeholder="可选：写下你的评价..."
      />
      <button
        type="submit"
        className="bg-indigo-600 text-white px-4 py-1.5 rounded-lg text-sm hover:bg-indigo-700"
      >
        提交评价
      </button>
    </form>
  )
}
