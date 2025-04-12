import { get, post } from "@/services/api";

const baseUrl = "/users";

const getAllUsers = () => {
  return get({ endpoint: `${baseUrl}` });
};

const getCurrentUser = () => {
  return get({ endpoint: `${baseUrl}/me` });
};

const login = (data) => {
  return post({
    endpoint: `${baseUrl}/auth`,
    data,
    extraHeaders: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    noAuth: true,
  });
};

const createUser = (data) => {
  return post({ endpoint: `${baseUrl}/new`, data, noAuth: true });
};

export { getAllUsers, getCurrentUser, login, createUser };
