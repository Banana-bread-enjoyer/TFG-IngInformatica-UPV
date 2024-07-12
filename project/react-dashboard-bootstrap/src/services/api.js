import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export const fetchItems = async () => {
  const response = await api.get("/items/");
  return response.data;
};

export default api;
