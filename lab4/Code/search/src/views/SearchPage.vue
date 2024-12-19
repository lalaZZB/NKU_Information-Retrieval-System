<template>
  <div class="search">
    <!-- 左侧的图片 -->
    <div class="left">
      <img src="./../assets/NKUGO.png" @click="goHome" />
    </div>

    <!-- 右侧的搜索相关组件 -->
    <div class="right">
      <!-- 将三个按钮放在同一行，并保持其他内容不变 -->
      <div class="switches">
        <a-switch
          :checked="isWildcardSearch"
          @change="toggleWildcard"
          style="margin-right: 15px"
        />通配查询
        <a-switch
          :checked="isRealPhraseSearch"
          @change="toggleRealPhraseSearch"
          style="margin-right: 15px"
        />短语查询
        <a-switch
          :checked="isPhraseSearch"
          @change="togglePhrase"
        />高级查询
      </div>

      <a-input-search
        v-focus
        v-model="searchText"
        size="large"
        @search="searchResult"
        placeholder="请输入搜索内容..."
        style="margin-bottom: 20px"
      />

      <!-- 描述信息 -->
      <p v-if="isWildcardSearch" class="wildcard-description">
        通配查询可以使用 * 代表任意字符，? 代表一个字符。
      </p>
      <p v-if="isRealPhraseSearch" class="realPhraseSearch-description">
        短语查询可以用来精确匹配用户输入的完整短语。
      </p>

      <!-- 短语查询表单 -->
      <a-row v-if="isPhraseSearch" class="phrase-search-form" gutter="16">
        <a-col :span="24" class="phrase-search-keywords">
          <a-input placeholder="请输入关键词..." v-model="keywords" />
        </a-col>
        <a-col :span="24">
          <a-input placeholder="起始日期..." v-model="startDate" />
        </a-col>
        <a-col :span="24">
          <a-input placeholder="截止日期..." v-model="endDate" />
        </a-col>
        <a-col :span="24">
          <a-input placeholder="来源媒体..." v-model="media" />
        </a-col>
        <a-col :span="24">
          <a-input placeholder="排除内容..." v-model="excludedContent" />
        </a-col>
        <a-col :span="24" class="phrase-search-button">
          <a-button type="primary" @click="searchResult">短语搜索</a-button>
        </a-col>
      </a-row>

      <!-- 查询结果部分 -->
<div v-if="result.length > 0" class="search-results">
  <div v-for="item in result" :key="item.id" class="search-result-card">
    <SearchResult :info="item"></SearchResult>
  </div>
</div>

<!-- 如果没有查询结果并且有输入的搜索内容 -->
<div v-else-if="searchText" class="no-results">
  <p>没有找到相关结果，请尝试修改搜索条件。</p>
</div>

<!-- 如果没有输入搜索内容 -->
<div v-else class="no-search-text">
  <p>请输入搜索内容以获取结果。</p>
</div>

    </div>
  </div>
</template>

<script>
import axios from "axios";
import SearchResult from "../components/SearchResult";

export default {
  name: "SearchPage",
  data() {
    return {
      searchText: "",
      result: [],
      isWildcardSearch: false,
      isRealPhraseSearch: false, // 新增的状态变量
      isPhraseSearch: false,
      keywords: "",
      startDate: "",
      endDate: "",
      media: "",
      excludedContent: "",
    };
  },
  components: {
    SearchResult,
  },
  methods: {
    toggleWildcard(value) {
      this.isWildcardSearch = value;
      if (value) {
        this.isRealPhraseSearch = false;
        this.isPhraseSearch = false;
      }
    },
    toggleRealPhraseSearch(value) {
      this.isRealPhraseSearch = value;
      if (value) {
        this.isWildcardSearch = false;
        this.isPhraseSearch = false;
      }
    },
    togglePhrase(value) {
      this.isPhraseSearch = value;
      if (value) {
        this.isWildcardSearch = false;
        this.isRealPhraseSearch = false;
      }
    },
    goHome() {
      this.$router.push("/").catch((err) => {
        if (err.name !== "NavigationDuplicated") {
          throw err;
        }
      });
    },
    searchResult() {
      if (this.searchText !== "") {
        this.$router
          .push({
            path: `/search`,
            query: {
              q: this.searchText,
              wildcard: this.isWildcardSearch,
              phrase: this.isPhraseSearch,
              realPhraseSearch: this.isRealPhraseSearch,  // 传递真实短语查询的状态
              keywords: this.keywords,
              startDate: this.startDate,
              endDate: this.endDate,
              media: this.media,
              excludedContent: this.excludedContent,
            },
          })
          .catch((err) => {
            if (err.name !== "NavigationDuplicated") {
              throw err;
            }
          });
      }

      const path = `http://localhost:5000/search?q=${encodeURIComponent(
        this.searchText
      )}&wildcard=${this.isWildcardSearch}&phrase=${
        this.isPhraseSearch
      }&realPhraseSearch=${this.isRealPhraseSearch}&keywords=${this.keywords}&startDate=${this.startDate}&endDate=${
        this.endDate
      }&media=${this.media}&excludedContent=${this.excludedContent}`;

      axios
        .get(path)
        .then((res) => {
          this.result = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.searchText = this.$route.query.q || "";
    this.isWildcardSearch = this.$route.query.wildcard === "true";
    this.isPhraseSearch = this.$route.query.phrase === "true";
    this.isRealPhraseSearch = this.$route.query.realPhraseSearch === "true"; // 读取 realPhraseSearch 的状态
    this.keywords = this.$route.query.keywords;
    this.startDate = this.$route.query.startDate;
    this.endDate = this.$route.query.endDate;
    this.media = this.$route.query.media;
    this.excludedContent = this.$route.query.excludedContent;
    this.searchResult();
  },
  watch: {
    "$route.query"(newQuery) {
      this.searchText = newQuery.q || "";
      this.isWildcardSearch = newQuery.wildcard === "true";
      this.isPhraseSearch = newQuery.phrase === "true";
      this.isRealPhraseSearch = newQuery.realPhraseSearch === "true"; // 更新 realPhraseSearch 状态
      this.keywords = newQuery.keywords;
      this.startDate = newQuery.startDate;
      this.endDate = newQuery.endDate;
      this.media = newQuery.media;
      this.excludedContent = newQuery.excludedContent;
      this.searchResult();
    },
  },
};
</script>

<style scoped>
.search {
  padding-top: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.left {
  width: 100%;
  text-align: center;
}

.left img {
  width: 300px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.left img:hover {
  transform: scale(1.1); /* 图片放大效果 */
}

.right {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 900px; /* 增加宽度限制 */
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.switches {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 500px; /* 调整按钮的最大宽度 */
  margin-bottom: 20px;
}

.switches a-switch {
  font-size: 16px;
}

.a-input-search {
  margin-bottom: 20px;
  max-width: 500px;
}

.wildcard-description,
.realPhraseSearch-description {
  color: #666;
  margin-top: 10px;
  font-size: 14px;
}

.phrase-search-form .ant-input,
.phrase-search-form .ant-picker {
  width: 100%;
}

.phrase-search-keywords {
  margin-top: 10px;
}

.phrase-search-button {
  margin-top: 20px;
}

.search-results {
  width: 100%;


  max-width: 900px;
  margin-top: 20px;
}

.search-result-card {
  background-color: #f9f9f9;
  padding: 20px;
  margin-bottom: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.search-result-card:hover {
  transform: translateY(-5px); /* 卡片悬浮效果 */
}

.search-result-card .title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.search-result-card .description {
  font-size: 16px;
  color: #666;
  line-height: 1.6;
}

.search-result-card .media_name {
  font-size: 14px;
  color: #007bff;
  font-style: italic;
  margin-top: 10px;
}

.no-results {
  font-size: 18px;
  color: #888;
  margin-top: 30px;
}

.search-result img {
  max-width: 100%;
  border-radius: 8px;
}



</style>