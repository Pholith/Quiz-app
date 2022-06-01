var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import axios, {} from "axios";
var config = {
    baseURL: `${import.meta.env.VITE_API_URL}`,
    //json: true,
};
const instance = axios.create(config);
export default {
    call(method, resource, data = null, token = null) {
        return __awaiter(this, void 0, void 0, function* () {
            var headers = {
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
                .then((response) => {
                return { status: response.status, data: response.data };
            })
                .catch((error) => {
                console.error(error);
            });
        });
    },
    // ------------------------------------------------
    // Partie contenant les routes des API à utiliser
    // ------------------------------------------------
    getQuizInfo() {
        return this.call("get", "quiz-info");
    },
    getQuestion(position) {
        return '{ "Quel est blabla", "titre", "image", 1}';
        return this.call("get", "questions/" + position);
    }
};
