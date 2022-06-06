import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import QuestionManager from '../views/QuestionManager.vue'
import EndPage from '../views/EndPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/start-new-quiz",
      name: "NewQuizPage",
      component: NewQuizPage,

    },
    {
      path: "/question",
      name: "QuestionManager",
      component: QuestionManager,
    },
    {
      path: "/end",
      name: "EndPage",
      component: EndPage,
    }
    // ... autres routes
  ]
});

export default router
