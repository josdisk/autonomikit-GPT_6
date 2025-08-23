import "./../styles/globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "AutonomiKit Dashboard",
  description: "Minimal Next.js UI for AutonomiKit-GPT",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="container">
          <header className="mb-6">
            <h1 className="text-3xl font-bold tracking-tight">AutonomiKit Dashboard</h1>
            <p className="text-slate-300">Call the FastAPI agent and view results.</p>
          </header>
          {children}
          <footer className="mt-10 text-sm text-slate-400">
            MIT © {new Date().getFullYear()} — Built for OSS portfolios
          </footer>
        </div>
      </body>
    </html>
  );
}
