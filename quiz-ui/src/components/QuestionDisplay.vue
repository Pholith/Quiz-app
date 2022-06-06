<template>
  <div class="question-display">
    <div class="question-display__question">
      <h2>{{ question.text }} </h2>
    </div>
    <img v-if="question.image" :src="question.image" />
    <div class="question-display__answers">
      <div v-for="(answer, index) in question.possibleAnswers" class="question-display__answer"
        @click="answerClickedHandler(index + 1)">
        <h3>{{ answer.text }}</h3>
      </div>
    </div>
  </div>

</template>

<script lang="ts">

export default {

  data(): any {
    return {
    };
  },
  props: {
    question: {
      type: Object,
      required: true,
    }
  },
  methods: {
    answerClickedHandler(answerId: number) {
      this.$emit('answer-selected', answerId);
    },
  },
  emits: ['answer-selected'],

}
</script>
