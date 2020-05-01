<template>
  <div id="main_content">
    <div id="search_block">
      <p>输入关键词，如‘好吃’，点击搜索，即可获取情感分析结果</p>
      <br />
      <a-input-search v-model="keyword" placeholder="请输入关键词" @search="onSearch" enterButton />
      <br />
      <br />
    </div>

    <div id="result_block" v-if="seen">
      <div id="chartPie" class="pie-wrap"></div>
      <p>共{{ sum_num }}条评论包含关键词:{{keyword}}，正面{{ positive_num }}条，负面{{ negative_num }}条</p>
      <br />
      <br />

      <a-table
        :columns="columns"
        :dataSource="comments"
        :pagination="{ pageSize: 50 }"
        :scroll="{ y: 240 }"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import echarts from "echarts";
require("echarts/theme/macarons"); //引入主题

const columns = [
  {
    title: "评论内容",
    dataIndex: "comment_content",
    width: 200
  },
  {
    title: "情感分析",
    dataIndex: "emotion",
    width: 50
  }
];

export default {
  data() {
    return {
      seen: false,
      keyword: "",
      chartPie: null,
      sum_num: "",
      positive_num: "",
      negative_num: "",
      comments: [],
      columns
    };
  },

  methods: {
    onSearch(value) {
      console.log(value);
      this.search_comments(value);
      this.seen = true;
    },

    search_comments(value) {
      const path = "http://localhost:5000";
      axios
        .get(path, {
          params: {
            keyword: value
          }
        })
        .then(res => {
          this.sum_num = res.data.sum_num;
          this.positive_num = res.data.positive_num;
          this.negative_num = res.data.negative_num;
          this.comments = res.data.comments;
          this.drawPieChart();
        });
    },

    drawPieChart() {
      let mytextStyle = {
        color: "#333",
        fontSize: 18
      };
      let mylabel = {
        show: true,
        position: "right",
        offset: [30, 40],
        formatter: "{b} : {c} ({d}%)",
        textStyle: mytextStyle
      };
      this.chartPie = echarts.init(
        document.getElementById("chartPie"),
        "macarons"
      );
      this.chartPie.setOption({
        title: {
          text: "情感分析结果",
          x: "center"
        },
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
          data: ["正面", "负面"],
          left: "center",
          top: "bottom",
          orient: "horizontal"
        },
        series: [
          {
            name: "访问来源",
            type: "pie",
            radius: ["50%", "70%"],
            center: ["50%", "50%"],
            data: [
              { value: this.positive_num, name: "正面" },
              { value: this.negative_num, name: "负面" }
            ],
            animationEasing: "cubicInOut",
            animationDuration: 2600,
            label: {
              emphasis: mylabel
            }
          }
        ]
      });
    }
  }
};
</script>

<style scoped>
div#main_content {
  width: 90%;
  margin-left: auto;
  margin-right: auto;
}

div#search_block {
  width: 40%;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.pie-wrap {
  width: 100%;
  height: 200px;
}
</style>