<template>
  <div>
    <a-card
      hoverable
      @click="goToDetailedPage"
      class="search-result-card"
    >
      <a-card-meta
        :title="info._source.title"
        :description="info._source.ctime"
      >
        <template #avatar>
          <a-avatar
            shape="square"
            style="background-color: #dEE82EE; width: 60px; height: 30px; font-size: 14px;"
          >
            {{ info._source.media_name || '新闻' }}
          </a-avatar>
        </template>
      </a-card-meta>

      <!-- 修改描述部分 -->
      <div class="describe">
        {{ info._source.content.slice(0, 200) + '...' }}
      </div>

      <!-- 显示关键词 -->
      <div class="score">
        <strong>关键词:</strong> {{ info._source.keywords }}
      </div>
    </a-card>
  </div>
</template>

<script>
export default {
  name: "SearchResult",
  props: ["info"],

  methods: {
    goToDetailedPage() {
      // 导航到详细页面
      this.$router.push({
        path: `/detailed`,
        query: {
          id: this.info._id,
          title: this.info._source.title,
          ctime: this.info._source.ctime,
          media_name: this.info._source.media_name || '新闻',
          content: this.info._source.content,
          keywords: this.info._source.keywords,
        }
      })
      .catch((err) => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
    },
  },
};
</script>

<style scoped>
/* 为卡片增加边框阴影，使其更有层次感 */
.search-result-card {
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 16px; /* 增加卡片之间的间距 */
}

/* 标题字体增大，突出显示 */
.ant-card-meta-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

/* 描述部分：增加字号、调整颜色、左对齐 */
.describe {
  padding: 10px 0;
  text-align: left; /* 左对齐文本 */
  font-size: 14px;
  color: #555; /* 使用更柔和的颜色 */
  line-height: 1.6; /* 增加行间距 */
  margin-bottom: 10px; /* 增加描述和评分之间的间距 */
}

/* 评分部分：右对齐，增加字号和样式 */
.score {
  font-size: 14px;
  color: #999; /* 更柔和的颜色 */
  text-align: right;
  margin-top: 10px;
}

/* 改变长方形头像的尺寸 */
.ant-avatar-square {
  background-color: #EE82EE;
  width: 60px;
  height: 30px;
  font-size: 14px;
}

/* 提升整体卡片的间距，提升可读性 */
.ant-card-meta {
  margin-bottom: 12px;
}
</style>