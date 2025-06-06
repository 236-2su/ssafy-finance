import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore("user", {
  state: () => ({
    isLogin: localStorage.getItem("isLogin") === "true",
    username: localStorage.getItem("username") || "",
    email: localStorage.getItem("email") || "",
    user: null, // { username, email, ..., interested_stocks: [] } 형태를 기대
    isValidating: false,
  }),
  actions: {
    login(username, email = "") {
      this.isLogin = true;
      this.username = username;
      localStorage.setItem("isLogin", "true");
      localStorage.setItem("username", username);

      if (email) {
        this.email = email;
        localStorage.setItem("email", email);
      } else {
        // email이 제공되지 않으면 기존 email 상태를 유지하거나, 명시적으로 초기화할 수 있습니다.
        // 여기서는 localStorage에서 email을 제거하고 상태도 초기화합니다.
        this.email = "";
        localStorage.removeItem("email");
      }
      // this.user 객체는 fetchUserProfile을 통해 상세 정보로 채워지므로,
      // login 액션에서는 isLogin, username, email 및 localStorage만 관리합니다.
      // 만약 login 시점에 user 객체의 일부를 업데이트해야 한다면,
      // 예를 들어 this.user = { ...this.user, username, email }; 와 같이 할 수 있으나,
      // 현재 구조에서는 fetchUserProfile이 user 객체 전체를 담당합니다.
    },
    logout() {
      this.isLogin = false;
      this.username = "";
      this.email = "";
      this.user = null; // 사용자 정보 초기화
      localStorage.removeItem("isLogin");
      localStorage.removeItem("username");
      localStorage.removeItem("email");
      // 추가적으로 user 관련 localStorage 항목이 있다면 여기서 모두 제거
    },
    async validateSession() {
      if (this.isValidating) return;

      this.isValidating = true;
      try {
        const response = await axios.get("/api/accounts/current-user/", {
          validateStatus: function (status) {
            // 모든 2xx, 401, 403 상태 코드를 성공으로 처리하여 catch 블록으로 가지 않도록 함
            return (
              (status >= 200 && status < 300) ||
              status === 401 ||
              status === 403
            );
          },
        });

        if (response.status === 200 && response.data.is_authenticated) {
          // 세션 유효 시, 전체 프로필 정보를 다시 가져와 user 상태를 최신으로 유지
          // fetchUserProfile 내부에서 user 상태가 업데이트됨
          await this.fetchUserProfile();
          // fetchUserProfile이 성공적으로 user 정보를 가져왔다면 this.user가 설정됨
          // username이 유효한 문자열인지 확인
          if (
            this.user &&
            typeof this.user.username === "string" &&
            this.user.username.trim() !== ""
          ) {
            // fetchUserProfile에서 이미 this.user.username과 this.user.email을 state에 반영했을 수 있으나,
            // login 액션을 호출하여 isLogin 상태와 localStorage를 일관되게 업데이트합니다.
            this.login(this.user.username, this.user.email || "");
            return true;
          } else {
            // fetchUserProfile 실패 또는 user 정보 (특히 username) 누락
            console.error(
              "User data (username) not found or invalid after fetching profile in validateSession. User object:",
              this.user
            );
            this.logout(); // 사용자 정보가 없으므로 로그아웃 처리
            return false;
          }
        } else if (response.status === 401 || response.status === 403) {
          // 401 또는 403 응답: 인증되지 않음 (콘솔 오류 없이 로그아웃)
          this.logout();
          return false;
        } else {
          // 200 응답이지만 is_authenticated가 false이거나, validateStatus에 포함되지 않은 다른 오류 코드
          // (예: 5xx 서버 오류는 validateStatus에 의해 여기로 오지 않고 catch로 감)
          // 혹은 is_authenticated 필드가 없는 경우 등 예외 케이스
          console.warn(
            "Session validation returned unexpected status or data:",
            response
          );
          this.logout();
          return false;
        }
      } catch (error) {
        // 네트워크 오류 또는 validateStatus에서 처리하지 않은 서버 오류 (예: 5xx)
        // 이 경우 axios는 기본적으로 콘솔에 오류를 출력할 수 있음
        // 명시적으로 제어하고 싶다면 error.config.silent 같은 플래그 사용 고려 (axios 플러그인 필요)
        // 또는 여기서 console.error를 조건부로 호출
        if (
          !error.isAxiosError ||
          (error.response &&
            error.response.status !== 401 &&
            error.response.status !== 403)
        ) {
          console.error("Session validation network/server error:", error);
        }
        this.logout();
        return false;
      } finally {
        this.isValidating = false;
      }
    },
    async checkAuthAndRedirect(router, redirectPath = "/login") {
      // isLogin 플래그를 먼저 확인 (빠른 실패)
      if (!this.isLogin) {
        router.push(redirectPath);
        return false;
      }
      // 서버에 실제 세션 유효성 검증
      const isValidSession = await this.validateSession();
      if (!isValidSession) {
        router.push(redirectPath);
        return false;
      }
      return true;
    },
    async fetchUserProfile() {
      // validateSession에서 이미 사용자가 인증되었음을 (is_authenticated: true) 확인한 후 호출되므로,
      // 여기서는 this.isLogin 상태에 의존하지 않고 프로필 정보를 가져오도록 시도합니다.
      // this.isLogin 상태는 localStorage에서 초기화되거나 login 액션에서 설정되는데,
      // 로그인 직후 validateSession -> fetchUserProfile 흐름에서는 아직 true가 아닐 수 있습니다.
      try {
        const response = await axios.get("/api/accounts/profile/");

        if (
          response.data &&
          typeof response.data.username === "string" &&
          response.data.username.trim() !== ""
        ) {
          this.user = response.data;

          // interested_stocks 처리
          if (this.user && !Array.isArray(this.user.interested_stocks)) {
            console.warn(
              "user.interested_stocks가 배열이 아닙니다. 빈 배열로 설정합니다:",
              this.user.interested_stocks
            );
            this.user.interested_stocks = [];
          }

          // Pinia 상태 업데이트
          this.username = this.user.username;
          this.email = this.user.email || ""; // email이 없을 경우 빈 문자열로
        } else {
          // 응답 데이터가 없거나 username이 유효하지 않은 경우
          console.warn(
            "Fetched profile data is invalid or username is missing. Response data:",
            response.data
          );
          this.user = null;
          this.username = "";
          this.email = "";
          // 이 경우 validateSession에서 logout 처리될 것임
        }
        return this.user; // 성공 시 user 객체, 실패 또는 데이터 이상 시 null 반환 가능성 있음
      } catch (error) {
        console.error("Failed to fetch user profile:", error);
        this.user = null; // 오류 발생 시 user 상태 초기화
        this.username = "";
        this.email = "";

        if (error.response?.status === 401 || error.response?.status === 403) {
          // 인증 오류 시 logout()을 호출하여 localStorage까지 정리
          this.logout();
        }
        // 오류를 다시 throw하여 호출 측에서 인지하도록 함
        // validateSession은 이 throw된 오류를 catch하여 logout 처리함
        throw error;
      }
    },
    // 관심 주식 추가 액션
    async addStockToWatchlist(stockName) {
      if (!this.isLogin || !this.user) {
        console.error("사용자 로그인 필요");
        throw new Error("로그인이 필요합니다.");
      }
      try {
        await axios.post("/api/accounts/stocks/", { stock_name: stockName });
        if (this.user && Array.isArray(this.user.interested_stocks)) {
          if (!this.user.interested_stocks.includes(stockName)) {
            this.user.interested_stocks.push(stockName);
          }
        } else if (this.user) {
          // interested_stocks가 없거나 배열이 아닌 경우
          this.user.interested_stocks = [stockName];
        }
        // 상태 변경을 감지하도록 새 배열 할당 (선택적)
        // this.user = { ...this.user, interested_stocks: [...this.user.interested_stocks] };
      } catch (error) {
        console.error(`Failed to add stock ${stockName} to watchlist:`, error);
        throw error;
      }
    },
    // 관심 주식 제거 액션
    async removeStockFromWatchlist(stockName) {
      if (
        !this.isLogin ||
        !this.user ||
        !Array.isArray(this.user.interested_stocks)
      ) {
        console.error("사용자 로그인 또는 관심 목록 초기화 필요");
        throw new Error("로그인이 필요하거나 관심 목록이 없습니다.");
      }
      try {
        // DELETE 요청 시 body 대신 params나 data를 사용 (서버 구현에 따라 다름)
        // Django REST framework는 기본적으로 DELETE 요청의 body를 파싱하지 않을 수 있음.
        // 여기서는 views.py에서 request.data.get("stock_name")을 사용하므로 data로 전달
        await axios.delete("/api/accounts/stocks/", {
          data: { stock_name: stockName },
        });

        const index = this.user.interested_stocks.indexOf(stockName);
        if (index > -1) {
          this.user.interested_stocks.splice(index, 1);
        }
        // 상태 변경을 감지하도록 새 배열 할당 (선택적)
        // this.user = { ...this.user, interested_stocks: [...this.user.interested_stocks] };
      } catch (error) {
        console.error(
          `Failed to remove stock ${stockName} from watchlist:`,
          error
        );
        throw error;
      }
    },
  },
});
