import { StatusBar } from 'expo-status-bar';
import { LoginScreen } from './src/screens/LoginScreen';

// App móvil base: se agregará navegación y autenticación real en próximas partes.
export default function App() {
  return (
    <>
      <LoginScreen />
      <StatusBar style="auto" />
    </>
  );
}
