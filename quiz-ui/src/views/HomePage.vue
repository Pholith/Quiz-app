<template>
  <h1>Home page</h1>

  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <router-link to="/start-new-quiz">Démarrer le quiz !</router-link>
</template>



<script lang="ts">
var registeredScores: number[] = [];

export default {
  data() {
    return {
      registeredScores
    };
  },

  async created() {
    console.log("Composant Home page 'created'");
  }
};
</script>


<style>
</style>