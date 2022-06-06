<template>
  <h1 v-if="isFullyLoaded"> Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <div v-if="isFullyLoaded">
    <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />

  </div>

</template>

<script lang="ts">
import router from "../router";
import QuizApiService from "../services/QuizApiService";
import QuestionDisplay from "../components/QuestionDisplay.vue";
import { ParticipationStorageService } from "../services/ParticipationStorageService";

var answers: number[] = [];

export default {
  data() {
    return {
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 0,
      currentQuestion: null,
      isFullyLoaded: false,
    };
  },

  methods: {

    async answerClickedHandler(answerId: number) {
      answers.push(answerId);
      if (this.currentQuestionPosition < this.totalNumberOfQuestion) {
        this.currentQuestionPosition++;
        this.loadQuestionByPosition(this.currentQuestionPosition);

      } else {
        this.endQuiz();
      }
    },
    async loadQuestionByPosition(position: number) {
      console.log("loadQuestionByPosition");
      this.currentQuestion = (await QuizApiService.getQuestion(position))?.data;
      this.totalNumberOfQuestion = await QuizApiService.getTotalNumberOfQuestions();
      console.log("end of loadQuestion:");
      console.log(this.currentQuestion);
      this.isFullyLoaded = true;

    },
    async endQuiz() {
      QuizApiService.addParticipation({ playerName: ParticipationStorageService.getPlayerName(), answers: answers });
      router.push('/end');
    },
  },

  components: {
    QuestionDisplay
  },
  created() {
    console.log("created");
    this.loadQuestionByPosition(1);
  }
}
</script>

<style>
</style>
