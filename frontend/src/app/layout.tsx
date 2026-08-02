import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Synovia - Your Autonomous AI Co-Founder",
  description: "Autonomous multi-agent system that turns startup ideas into investor-ready blueprints in seconds.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-[#080c14] text-slate-100 min-h-screen">
        {children}
      </body>
    </html>
  );
}
