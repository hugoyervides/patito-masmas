import './globals.css';

export const metadata = {
  title: 'Patito ++ Web IDE',
  description: 'Editor y entorno de ejecucion en linea para el lenguaje Patito ++',
  icons: {
    icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🦆</text></svg>",
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
