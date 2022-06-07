<template>

  <div class="newQuiz mb-5">
    <p> Insérez votre pseudo </p>
    <input type="text" class="form-control" v-model="username" placeholder="Nom du joueur" />
    <button @click="launchNewQuiz" type="button" class="btn btn-primary"> Go ! </button>
  </div>
</template>

<script lang="ts">

import { ParticipationStorageService } from "../services/ParticipationStorageService";
import router from "../router";

export default {
  data() {
    return {
      username: ""
    };
  },

  methods: {
    launchNewQuiz() {
      ParticipationStorageService.savePlayerName(this.username);
      router.push('/question');
    },
  },

  async created() {
    console.log("Composant NewQuiz page 'created'");
  }
};
</script>


<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
