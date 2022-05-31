export class ParticipationStorageService {
    static clear() {
        window.localStorage.clear();
    }
    static savePlayerName(playerName) {
        window.localStorage.setItem("playerName", playerName);
    }
    static getPlayerName() {
        var _a;
        return (_a = window.localStorage.getItem("playerName")) !== null && _a !== void 0 ? _a : "";
    }
    static saveParticipationScore(participationScore) {
        window.localStorage.setItem("participationScore", participationScore.toString());
    }
    static getParticipationScore() {
        var _a;
        return (_a = window.localStorage.getItem("participationScore")) !== null && _a !== void 0 ? _a : 0;
    }
}
