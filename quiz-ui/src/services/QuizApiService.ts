import axios, { type AxiosRequestConfig, type AxiosInstance } from "axios";

var config: AxiosRequestConfig = {
  baseURL: `${import.meta.env.VITE_API_URL}`,
  //json: true,
}

const instance: AxiosInstance = axios.create(config);

export default {
  async call(method: any, resource: any, data = null, token = null) {
    var headers: any = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response: any) => {
        return { status: response.status, data: response.data };
      })
      .catch((error: any) => {
        console.error(error);
      });
  },

  // ------------------------------------------------
  // Partie contenant les routes des API à utiliser
  // ------------------------------------------------

  getQuizInfo() {
    return this.call("get", "quiz-info");
  },

  getQuestion(position: number) {
    return '{ "Quel est blabla", "titre", "image", 1}'
    return this.call("get", "questions/" + position);
  }
};