import Vue from 'vue'
import Router from 'vue-router'
import InputSearch from '@/components/InputSearch'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'InputSearch',
      component: InputSearch
    }
  ]
})
