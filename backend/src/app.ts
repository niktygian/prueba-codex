import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';

// App base de Express. Las rutas reales se completan en las próximas partes.
export const createApp = () => {
  const app = express();

  app.use(helmet());
  app.use(cors());
  app.use(express.json());
  app.use(morgan('dev'));

  app.get('/health', (_req, res) => {
    res.json({ status: 'ok', service: 'control360-backend' });
  });

  // Namespace base de API.
  app.get('/api', (_req, res) => {
    res.json({
      message: 'API base de Control360 Almacenes',
      version: '0.1.0'
    });
  });

  return app;
};
