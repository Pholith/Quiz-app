<template>
  <div class="endPage">
    <p v-if="score != -1">Votre score: {{ score }}</p>
  </div>
</template>

<script lang="ts">

import { ParticipationStorageService } from "../services/ParticipationStorageService";
import QuizApiService from "../services/QuizApiService";

export default {
  data() {
    return {
      score: -1,
    };
  },

  methods: {
    launchNewQuiz() {
    },
  },

  created() {
    QuizApiService.getPlayerParticipation(ParticipationStorageService.getPlayerName())
      .then((score: number) => {
        this.score = score;
        console.log("score récupéré: ", this.score);
      });
  },
}
</script>