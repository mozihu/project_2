<template>
  <div id="main_content">
    <div id="search_block">
      <p>输入关键词，如‘好吃’，点击搜索</p>
      <a-input-search placeholder="请输入关键词" @search="onSearch" enterButton />
      <br />
      <br />
    </div>

    <div id="result_block" v-if="seen">
      <div id="chartPie" class="pie-wrap"></div>
      <p>共{{ sum_num }}条评论包含关键词:{{keyword}}，正面{{ positive_num }}条，负面{{ negative_num }}条</p>
      <br />

      <a-table :columns="columns" :data-source="comments" @change="onChange" />
    </div>
  </div>
</template>

<script>
import axios from "axios";

// import echarts from "echarts";
import echarts from "echarts/lib/echarts";
require("echarts/lib/chart/pie");
require("echarts/lib/component/tooltip");
// require("echarts/theme/macarons"); //引入主题

const columns = [
  {
    title: "日期",
    dataIndex: "date",
    width: 50
  },
  {
    title: "评论内容",
    dataIndex: "comment_content",
    width: 150
  },
  {
    title: "情感分析",
    dataIndex: "emotion",
    width: 50,
    filters: [
      {
        text: "正面",
        value: "正面"
      },
      {
        text: "负面",
        value: "负面"
      }
    ],
    filterMultiple: false,
    onFilter: (value, record) => record.emotion.indexOf(value) === 0
  }
];

function onChange(pagination, filters, sorter) {
  console.log("params", pagination, filters, sorter);
}

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
    onChange,

    search_comments(value) {
      this.keyword = value;
      const path = "http://l3132c3923.qicp.vip/";
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
        formatter: "{b}",
        textStyle: mytextStyle
      };
      this.chartPie = echarts.init(
        document.getElementById("chartPie"),
        "macarons"
      );
      this.chartPie.setOption({
        // title: {
        //   text: "情感分析结果",
        //   x: "center"
        // },
        tooltip: {
          trigger: "item",
          formatter: "{a} {b} : {c} ({d}%)"
        },
        // legend: {
        //   data: ["正面", "负面"],
        //   left: "center",
        //   top: "bottom",
        //   orient: "horizontal"
        // },
        series: [
          {
            name: "情感分析",
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
  display: block;
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
  width: 200px;
  height: 200px;
  margin-left: auto;
  margin-right: auto;
}
</style>