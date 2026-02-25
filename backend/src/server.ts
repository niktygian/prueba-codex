import { createApp } from './app';

const PORT = Number(process.env.PORT || 4000);
const app = createApp();

app.listen(PORT, () => {
  // Log simple inicial; será reemplazado por logger estructurado.
  console.log(`[Control360] Backend ejecutándose en puerto ${PORT}`);
});
