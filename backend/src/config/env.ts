// Configuración centralizada de variables de entorno (placeholder).
export const env = {
  nodeEnv: process.env.NODE_ENV ?? 'development',
  port: Number(process.env.PORT ?? 4000),
  jwtSecret: process.env.JWT_SECRET ?? 'changeme',
  dbUrl: process.env.DB_URL ?? 'sqlite://./database/control360.db',
  corsOrigin: process.env.CORS_ORIGIN ?? 'http://localhost:5173'
};
