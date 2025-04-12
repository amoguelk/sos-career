import { get } from "@/services/api";

const baseUrl = "/profiles";

const getAllProfiles = () => {
  return get({ endpoint: `${baseUrl}` });
};

const getCurrentProfile = () => {
  return get({ endpoint: `${baseUrl}/me` });
};

export { getAllProfiles, getCurrentProfile };
