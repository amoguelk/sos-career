import { get, post, patch } from "@/services/api";

const baseUrl = "/profiles";

const getAllProfiles = () => {
  return get({ endpoint: `${baseUrl}` });
};

const getCurrentProfile = () => {
  return get({ endpoint: `${baseUrl}/me` });
};

const createProfile = (data) => {
  return post({ endpoint: `${baseUrl}`, data });
};

const editProfile = (userId, data) => {
  return patch({ endpoint: `${baseUrl}/${userId}`, data });
};

export { getAllProfiles, getCurrentProfile, createProfile, editProfile };
