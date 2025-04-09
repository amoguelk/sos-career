import { get, post } from "@/services/api";

const getAllUsers = () => {
  return get("/users");
};

const login = (data) => {
  return post("/users/auth", data, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
};

const createUser = (data) => {
  return post("/users/new", data);
};

export { getAllUsers, login, createUser };
