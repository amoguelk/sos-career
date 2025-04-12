import axios from "axios";

const getAuthHeader = (extraHeaders = {}, noAuth = false) => {
  const token = JSON.parse(localStorage.getItem("access_token")) ?? null;
  if (noAuth || !token) return { ...extraHeaders };
  return { Authorization: `Bearer ${token}`, ...extraHeaders };
};

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Wrapper GET method
 * @param {object} options
 * @param {string} options.endpoint The endpoint URL
 * @param {object} [options.extraHeaders={}] Extra headers to add to the request
 * @param {boolean} [options.noAuth=false] Whether the request requires authentication
 * @return {Promise<AxiosResponse>}
 */
const get = ({ endpoint, extraHeaders = {}, noAuth = false }) => {
  const headers = getAuthHeader(extraHeaders, noAuth);
  return api.get(endpoint, { headers });
};

/**
 * Wrapper POST method
 * @param {object} options
 * @param {string} options.endpoint The endpoint URL
 * @param {object} [options.data={}] Data to send with the request
 * @param {object} [options.extraHeaders={}] Extra headers to add to the request
 * @param {boolean} [options.noAuth=false] Whether the request requires authentication
 * @return {Promise<AxiosResponse>}
 */
const post = ({ endpoint, data = {}, extraHeaders = {}, noAuth = false }) => {
  const headers = getAuthHeader(extraHeaders, noAuth);
  return api.post(endpoint, data, { headers });
};

/**
 * Wrapper PUT method
 * @param {object} options
 * @param {string} options.endpoint The endpoint URL
 * @param {object} [options.data={}] Data to send with the request
 * @param {object} [options.extraHeaders={}] Extra headers to add to the request
 * @param {boolean} [options.noAuth=false] Whether the request requires authentication
 * @return {Promise<AxiosResponse>}
 */
const put = ({ endpoint, data = {}, extraHeaders = {}, noAuth = false }) => {
  const headers = getAuthHeader(extraHeaders, noAuth);
  return api.put(endpoint, data, { headers });
};

/**
 * Wrapper DELETE method
 * @param {object} options
 * @param {string} options.endpoint The endpoint URL
 * @param {object} [options.data={}] Data to send with the request
 * @param {object} [options.extraHeaders={}] Extra headers to add to the request
 * @param {boolean} [options.noAuth=false] Whether the request requires authentication
 * @return {Promise<AxiosResponse>}
 */
const del = ({ endpoint, data = {}, extraHeaders = {}, noAuth = false }) => {
  const headers = getAuthHeader(extraHeaders, noAuth);
  return api.delete(endpoint, data, { headers });
};

export { get, post, put, del };
