<template>
  <div class="news-detail-container">
    <div class="header">
      <h1>{{ title }}</h1>
      <p class="meta">
        <span>{{ ctime }}</span> <span class="media-name">{{ media_name }}</span>
      </p>
    </div>
    <div class="content">
      <p>{{ content }}</p>
    </div>
    <div class="keywords">
      <p>
        <strong>关键字：</strong>
        <span class="keyword" v-for="keyword in keywordsList" :key="keyword">{{ keyword }}</span>
      </p>
    </div>
    <div class="action-buttons">
      <button @click="goBack" class="back-button">返回</button>
      <button @click="openSnapshot" class="snapshot-button">网页快照</button>
    </div>
    <div class="recommendations">
      <h2>推荐新闻</h2>
      <ul>
        <li v-for="news in recommendations" :key="news.url">
          <a :href="news.url" target="_blank">{{ news.title }}</a>
        </li>
      </ul>
    </div>
    <div class="footer">
      <p>© 2024 NKUGO BY ZZB</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "DetailedPage",

  data() {
    return {
      id: "",
      title: "",
      ctime: "",
      media_name: "",
      content: "",
      keywords: "",
      keywordsList: [],
      recommendations: []
    };
  },

  created() {
    this.fetchNewsDetail();
    this.fetchRecommendations();
  },

  methods: {
    goBack() {
      this.$router.go(-1);
    },
    openSnapshot() {
      const imageName = this.formatTitleToFilename(this.title);
      const url = `http://localhost:5000/open-snapshot?image_name=${imageName}`;

      axios.get(url)
        .then(response => {
          console.log('Snapshot opened:', response.data);
        })
        .catch(error => {
          console.error('There has been a problem with your axios operation:', error);
        });
    },
    formatTitleToFilename(title) {
      return title.replace(/\s+/g, '%20');
    },
    fetchNewsDetail() {
      if (this.$route.query) {
        this.id = this.$route.query.id;
        this.title = this.$route.query.title;
        this.ctime = this.$route.query.ctime;
        this.media_name = this.$route.query.media_name;
        this.content = this.$route.query.content;
        this.keywords = this.$route.query.keywords;
        this.keywordsList = this.keywords.split(","); // 假设关键字是以逗号分隔的
      }
    },
    fetchRecommendations() {
      axios.get(`http://localhost:5000/get-recommendations?id=${this.id}`)
        .then(response => {
          this.recommendations = response.data.recommendations;
        })
        .catch(error => {
          console.error('Error fetching recommendations:', error);
        });
    },
  },
};
</script>

<style scoped>
.news-detail-container {
  padding: 40px 60px;
  font-family: "Arial", sans-serif;
  background-color: #f4f7fb; /* 淡灰色背景 */
  color: #333;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  max-width: 800px;
  margin: 40px auto;
  position: relative;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

h1 {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50; /* 深色字体 */
  margin-bottom: 10px;
}

.meta {
  font-size: 14px;
  color: #7f8c8d;
}

.meta span {
  margin-right: 10px;
}

.content {
  font-size: 16px;
  line-height: 1.8;
  margin-top: 20px;
  color: #555;
}

.keywords {
  margin-top: 30px;
  color: #666;
}

.keyword {
  background-color: #e1e8f0;
  color: #3498db;
  padding: 6px 12px;
  margin-right: 8px;
  border-radius: 16px;
  font-size: 14px;
  display: inline-block;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.back-button, .snapshot-button {
  padding: 12px 24px;
  border-radius: 25px;
  border: none;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button {
  background-color: #27ae60;
  color: white;
}

.snapshot-button {
  background-color: #2980b9;
  color: white;
}

.back-button:hover, .snapshot-button:hover {
  opacity: 0.8;
}

.recommendations {
  margin-top: 40px;
}

.recommendations h2 {
  font-size: 22px;
  color: #2c3e50;
  margin-bottom: 15px;
}

.recommendations ul {
  list-style: none;
  padding: 0;
}

.recommendations li {
  margin-bottom: 10px;
}

.recommendations a {
  color: #2980b9;
  text-decoration: none;
  font-size: 16px;
  transition: all 0.3s ease;
}

.recommendations a:hover {
  text-decoration: underline;
}

.footer {
  margin-top: 40px;
  text-align: center;
  color: #7f8c8d;
}

@media screen and (max-width: 768px) {
  .news-detail-container {
    padding: 20px;
    margin: 20px;
  }

  .back-button, .snapshot-button {
    width: 48%;
    font-size: 14px;
  }

  .recommendations h2 {
    font-size: 20px;
  }

  .recommendations a {
    font-size: 14px;
  }
}
</style>