import { View, Text, TextInput, Button } from 'react-native';

// Pantalla placeholder de login.
export const LoginScreen = () => {
  return (
    <View style={{ flex: 1, justifyContent: 'center', padding: 20 }}>
      <Text style={{ fontSize: 24, marginBottom: 12 }}>Control360</Text>
      <TextInput placeholder="Usuario" style={{ borderWidth: 1, marginBottom: 8, padding: 8 }} />
      <TextInput placeholder="Contraseña" secureTextEntry style={{ borderWidth: 1, marginBottom: 12, padding: 8 }} />
      <Button title="Ingresar" onPress={() => {}} />
    </View>
  );
};
