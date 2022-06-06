import axios, { type AxiosRequestConfig, type AxiosInstance } from "axios";

var config: AxiosRequestConfig = {
  baseURL: `${import.meta.env.VITE_API_URL}`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
}

const instance: AxiosInstance = axios.create(config);

export default {
  async call(method: any, resource: any, data = null, token = null) {
    var headers: any = {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
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
    return this.call("get", "questions/" + position);
  },
  async getTotalNumberOfQuestions() {
    let infos = await this.call("get", "quiz-info")
    if (!infos)
      return 0;
    return infos.data["size"];
  },

  addParticipation(participation: any) {
    return this.call("post", "participations", participation);
  },

  getPlayerParticipation(playerName: string) {
    this.call("get", "quiz-info").then((response: any) => {
      return response.data["scores"].find((score: any) => {
        return score.playerName === playerName;
      });
    }, (error: any) => {
      console.error(error);
    });
  }
  // ------------------------------------------------

};