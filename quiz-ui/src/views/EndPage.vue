<template>
  <p>Your score: {{ score }}</p>
</template>

<script lang="ts">

import { ParticipationStorageService } from "../services/ParticipationStorageService";
import QuizApiService from "../services/QuizApiService";

export default {
  data() {
    return {
      score: 0,
    };
  },

  methods: {
    launchNewQuiz() {
    },
  },

  async created() {
    this.score = await QuizApiService.getPlayerParticipation(ParticipationStorageService.getPlayerName());
  },
}
</script>