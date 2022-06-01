<template>
  <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
  <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />

</template>

<script lang="ts">
import router from "../router";
import QuizApiService from "../services/QuizApiService";
import QuestionDisplay from "../components/QuestionDisplay.vue";

var currentQuestionPosition = 0;
var totalNumberOfQuestion = 1;
var currentQuestion: any = null;

export default {
  data() {
    return {
      currentQuestionPosition: currentQuestionPosition,
      totalNumberOfQuestion: totalNumberOfQuestion,
      currentQuestion: currentQuestion
    };
  },
  props: {
  },
  methods: {

    async answerClickedHandler(answerId: number) {
      if (currentQuestion.correctAnswerId === answerId) {
        console.log("Bonne réponse");
      } else {
        console.log("Mauvaise réponse");
      }
    },
    async loadQuestionByPosition(position: number) {
      console.log("loadQuestionByPosition");
      currentQuestion = await QuizApiService.getQuestion(position);
      currentQuestionPosition = position;
      let quizInfos = await QuizApiService.getQuizInfo();
    },
    async endQuiz() {
      router.push('/end');
    },
  },

  components: {
    QuestionDisplay
  },

  async created() {
    console.log("QuestionManager created");
    this.loadQuestionByPosition(currentQuestionPosition);
  },
}
</script>

<style>
</style>
