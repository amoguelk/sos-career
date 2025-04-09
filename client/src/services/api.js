import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Get method
 * @param {string} url The request endpoint
 * @returns
 */
const get = (url) => {
  return api.get(url);
};

const post = (url, data, config = {}) => {
  return api.post(url, data, config);
};

const put = (url) => {
  return api.put(url);
};

const remove = (url) => {
  return api.delete(url);
};

export { get, post, put, remove };
