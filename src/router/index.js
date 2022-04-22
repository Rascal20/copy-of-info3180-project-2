import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/explore',
      name: 'explore',
      component: () => import('../views/ExploreView.vue'),
      props: true
    },
    {
      path: '/users/:user_id',
      name: 'profile',
      component: () => import('../views/ProfileView.vue')
    },
    {
      path: '/cars/new',
      name: 'add-car',
      component: () => import('../views/AddCarView.vue')
    }
    //{
     // path: '/cars/:car_id',
     // name: 'view-car',
      //component: () => import('../views/CarView.vue')
    //}
  ]
})

export default router
