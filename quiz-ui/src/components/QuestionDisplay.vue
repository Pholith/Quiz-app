<template>
  <img v-if="question.image" :src="question.image" />
  <a @click="$emit('answer-selected', 2)">La réponse D</a>

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
