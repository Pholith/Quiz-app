<template>
  <img v-if="question.image" :src="question.image" />
  <a @click="$emit('answer-selected', 0)">La réponse A</a>
  <a @click="$emit('answer-selected', 1)">La réponse B</a>
  <a @click="$emit('answer-selected', 2)">La réponse C</a>
  <a @click="$emit('answer-selected', 3)">La réponse D</a>

</template>

<script lang="ts">

var question: any = {};

export default {
  data() {
    return { question };
  },
  emits: ['answer-selected'],

}
</script>
