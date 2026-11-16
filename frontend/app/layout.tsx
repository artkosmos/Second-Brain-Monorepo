import type { Metadata } from "next";
import { Geist, Newsreader } from "next/font/google";
import { Toaster } from "@/providers/toaster";
import "./globals.css";

const geist = Geist({
  variable: "--font-geist",
  subsets: ["latin"],
});

const newsreader = Newsreader({
  variable: "--font-newsreader",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Second Brain",
  description: "A quiet place for notes.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${geist.variable} ${newsreader.variable} h-full`}>
      <body className="h-full antialiased">
        {children}
        <Toaster />
      </body>
    </html>
  );
}
