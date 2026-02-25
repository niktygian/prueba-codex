import axios from 'axios';

// Cliente API base para consumir backend local.
export const apiClient = axios.create({
  baseURL: 'http://localhost:4000/api'
});
