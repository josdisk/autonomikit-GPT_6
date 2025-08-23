export default function ResultCard({ result }: { result: string }) {
  return (
    <div className="card mt-4">
      <div className="badge">Result</div>
      <div className="mt-2 whitespace-pre-wrap">{result || "No result yet."}</div>
    </div>
  );
}
