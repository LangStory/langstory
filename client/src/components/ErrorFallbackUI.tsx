export default function ErrorFallbackUI({error, resetError}: {
    error: Error | null,
    resetError: () => void
}) {
    return (
        <div className="w-full h-full flex flex-col justify-center items-center bg-white text-red-500 font-light space-y-6">
            <p className="text-2xl font-medium">Something went wrong</p>
            <p className="text-center">{error && error.message}</p>
            <button className="px-4 py-2 rounded bg-blue-500 text-white" onClick={resetError}>Try again</button>
        </div>
    )
}