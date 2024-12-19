<template>
  <div>
    <!-- 固定登录按钮或显示用户名 -->
    <div class="fixed-header">
      <!-- 显示登录按钮或用户名 -->
      <a-button v-if="!isLoggedIn" class="login-button" @click="showLoginModal">登录</a-button>
      <div v-else class="user-info">{{ username }}</div>
      <!-- 登录组件 -->
      <LoginComponent v-if="showLogin" @close="showLogin = false" @login-success="handleLoginSuccess" />
    </div>

    <div class="home">
      <!-- Logo 组件 -->
      <LogoComponent class="ha" />

      <!-- 搜索输入和按钮 -->
      <div class="search-input">
        <a-input-search
          size="large"
          placeholder="在 NKUGO 上搜索新闻"
          v-focus
          v-model="searchText"
          @search="onSearch"
          @focus="onSearchInputFocus"
          @blur="onSearchInputBlur"
        />

        <!-- 搜索历史下拉列表 -->
        <div v-if="showSearchHistory" class="search-history-dropdown">
          <ul>
            <li v-for="(item, index) in searchHistory" :key="index" @click="selectSearchHistory(item)">
              {{ item }}
            </li>
          </ul>
        </div>

        <!-- 搜索选项按钮 -->
        <div class="buttons">
          <a-button :class="{ active: isPhraseSearch }" @click="onPhraseSearch">高级查询</a-button>
          <a-button :class="{ active: isWildcardSearch }" @click="onWildcardSearch">通配查询</a-button>
          <a-button :class="{ active: isRealPhraseSearch }" @click="onRealPhraseSearch">短语查询</a-button>
        </div>

        <!-- 查询类型说明 -->
        <p v-if="isWildcardSearch" class="wildcard-description">
          通配查询可以使用 * 代表任意字符，? 代表一个字符。
        </p>
        <p v-if="isRealPhraseSearch" class="wildcard-description">
          短语查询可以用来精确匹配用户输入的完整短语
        </p>

        <!-- 短语查询表单 -->
        <div v-if="isPhraseSearch" class="phrase-search-form">
          <div class="form-item">
            <label>必须包含的关键词：</label>
            <a-input placeholder="关键词..." v-model="keywords" />
          </div>
          <div class="form-item">
            <label>起始日期：</label>
            <a-input placeholder="YYYY-MM-DD" v-model="startDate" />
          </div>
          <div class="form-item">
            <label>截止日期：</label>
            <a-input placeholder="YYYY-MM-DD" v-model="endDate" />
          </div>
          <div class="form-item">
            <label>来源媒体：</label>
            <a-input placeholder="媒体..." v-model="media" />
          </div>
          <div class="form-item">
            <label>不包含以下内容：</label>
            <a-input placeholder="不包含的内容..." v-model="excludedContent" />
          </div>
          <div class="form-item">
            <a-button type="primary" @click="onSearch">搜索</a-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LogoComponent from "@/components/LogoComponent.vue";
import LoginComponent from "@/components/LoginComponent.vue";
import axios from "axios";

export default {
  name: "HomePage",
  data() {
    return {
      searchText: "",
      isWildcardSearch: false,
      isPhraseSearch: false,
      isRealPhraseSearch: false,
      keywords: "",
      startDate: "",
      endDate: "",
      media: "",
      excludedContent: "",
      isLoggedIn: false,
      username: "",
      showLogin: false,
      searchHistory: [],
      showSearchHistory: false,
    };
  },
  components: {
    LogoComponent,
    LoginComponent,
  },
  methods: {
    fetchSearchHistory() {
      if (this.isLoggedIn) {
        axios
          .get(
            `http://localhost:5000/get-search-history?username=${encodeURIComponent(
              this.username
            )}`
          )
          .then((response) => {
            this.searchHistory = response.data.history;
            this.showSearchHistory = true;
          })
          .catch((error) => {
            console.error("Failed to fetch search history:", error);
          });
      }
    },
    onSearchInputFocus() {
      this.fetchSearchHistory();
    },
    onSearchInputBlur() {
      setTimeout(() => {
        this.showSearchHistory = false;
      }, 200);
    },
    handleLoginSuccess(username) {
      this.isLoggedIn = true;
      this.username = username;
      this.showLogin = false;
    },
    sendSearchToBackend(searchText) {
      const url = `http://localhost:5000/store-search-history`;
      axios
        .post(url, {
          username: this.username,
          searchText: searchText,
        })
        .then((response) => {
          console.log("Search history stored:", response.data);
        })
        .catch((error) => {
          console.error("Failed to store search history:", error);
        });
    },
    onSearch() {
      if (this.isLoggedIn) {
        this.searchHistory.push(this.searchText);
        this.sendSearchToBackend(this.searchText);
      }

      if (this.searchText !== "") {
        this.$router.push({
          path: `/search`,
          query: {
            q: this.searchText,
            wildcard: this.isWildcardSearch,
            phrase: this.isPhraseSearch,
            realPhraseSearch: this.isRealPhraseSearch,
            keywords: this.keywords,
            startDate: this.startDate,
            endDate: this.endDate,
            media: this.media,
            excludedContent: this.excludedContent,
          },
        });
      }
    },
    onPhraseSearch() {
      this.isWildcardSearch = false;
      this.isPhraseSearch = !this.isPhraseSearch;
      this.isRealPhraseSearch = false;
    },
    onWildcardSearch() {
      this.isPhraseSearch = false;
      this.isWildcardSearch = !this.isWildcardSearch;
      this.isRealPhraseSearch = false;
    },
    onRealPhraseSearch() {
      this.isRealPhraseSearch = !this.isRealPhraseSearch;
      this.isPhraseSearch = false;
      this.isWildcardSearch = false;
    },
    showLoginModal() {
      this.showLogin = !this.showLogin;
    },
  },
  directives: {
    focus: {
      inserted: function (el) {
        el.focus();
      },
    },
  },
};
</script>

<style scoped>
/* 固定头部样式 */
.fixed-header {
  position: fixed;
  top: 0;
  right: 0;
  padding: 20px;
  z-index: 1000;
}

.login-button {
  position: absolute;
  top: 20px;
  right: 20px;
}

.user-info {
  background-color: #f0f0f0;
  padding: 10px 15px;
  border-radius: 20px;
  color: #333;
}

/* 首页样式 */
.home {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  text-align: center;
  padding: 20px;
}

/* Logo组件 */
.ha {
  margin-bottom: 20px;
}

/* 搜索框样式 */
.search-input {
  width: 600px;
  margin: 0 auto;
}

/* 搜索历史下拉框样式 */
.search-history-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background-color: #fff;
  border: 1px solid #ccc;
  border-top: none;
  z-index: 10;
}

.search-history-dropdown ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.search-history-dropdown li {
  padding: 8px;
  cursor: pointer;
}

.search-history-dropdown li:hover {
  background-color: #f5f5f5;
}

/* 按钮样式 */
.buttons {
  margin-top: 20px;
}

a-button {
  margin: 0 10px;
}

a-button.active {
  background-color: #1890ff;
  color: white;
}

/* 查询类型说明 */
.wildcard-description {
  margin-top: 10px;
  color: #666;
}

/* 短语查询表单样式 */
.phrase-search-form {
  background: #fff;
  padding: 20px;
  margin-top: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-item {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}

.form-item label {
  min-width: 130px;
  text-align: right;
  margin-right: 10px;
}

/* 响应式调整 */
@media (max-width: 768px) {


 .search-input {
    width: 100%;
  }

  .home {
    width: 90%;
  }
}
</style>