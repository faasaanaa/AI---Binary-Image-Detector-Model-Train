import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'You See It, We Verify It',
  description: 'Minimal dark themed image verification frontend.'
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}