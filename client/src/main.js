// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
// import Antd from 'ant-design-vue';
// import 'ant-design-vue/dist/antd.css';
import { Input, Table } from 'ant-design-vue';
import 'ant-design-vue/lib/input/style/css';
import 'ant-design-vue/lib/table/style/css';

import App from './App'
import router from './router'

Vue.config.productionTip = false

// Vue.use(Antd);
Vue.use(Input);
Vue.use(Table);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
