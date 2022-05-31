export class ParticipationStorageService {

  static clear() {
    window.localStorage.clear();
  }
  static savePlayerName(playerName: string) {
    window.localStorage.setItem("playerName", playerName);
  }

  static getPlayerName(): string {
    return window.localStorage.getItem("playerName") ?? "";
  }

  static saveParticipationScore(participationScore: number) {
    window.localStorage.setItem("participationScore", participationScore.toString());
  }

  static getParticipationScore(): any {
    return window.localStorage.getItem("participationScore") ?? 0;
  }
}