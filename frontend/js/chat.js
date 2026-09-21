const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");
const loadingIndicator = document.getElementById("loadingIndicator");
const refreshSummaryBtn = document.getElementById("refreshSummaryBtn");

function formatNumber(value) {
  if (value === null || value === undefined) {
    return "-";
  }

  return Number(value).toLocaleString("ko-KR");
}

function formatTrend(trend) {
  const labels = {
    increasing: "📈 증가",
    decreasing: "📉 감소",
    stable: "➡️ 유지",
    no_data: "데이터 없음",
  };

  return labels[trend] || trend;
}

async function loadSummary() {
  try {
    const summary = await apiRequest("/api/data/summary");

    document.getElementById("summaryCount").textContent =
      formatNumber(summary.count);

    document.getElementById("summaryAverage").textContent =
      formatNumber(summary.average);

    document.getElementById("summaryMax").textContent =
      formatNumber(summary.max);

    document.getElementById("summaryLatest").textContent =
      formatNumber(summary.latest);

    document.getElementById("summaryTrend").textContent =
      formatTrend(summary.trend);

    document.getElementById("summaryPeriod").textContent =
      summary.start_date && summary.end_date
        ? `${summary.start_date} ~ ${summary.end_date}`
        : "-";
  } catch (error) {
    console.error(error);

    document.getElementById("summaryTrend").textContent =
      "불러오기 실패";
  }
}

function addMessage(role, content) {
  const wrapper = document.createElement("div");

  wrapper.className =
    role === "user"
      ? "message user-message"
      : "message assistant-message";

  const label = document.createElement("div");
  label.className = "message-label";
  label.textContent = role === "user" ? "YOU" : "AI";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  bubble.textContent = content;

  wrapper.appendChild(label);
  wrapper.appendChild(bubble);

  chatMessages.appendChild(wrapper);

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendChat(message) {
  loadingIndicator.classList.remove("hidden");

  try {
    const result = await apiRequest("/api/chat", {
      method: "POST",
      body: JSON.stringify({
        message,
      }),
    });

    addMessage("assistant", result.answer);
  } catch (error) {
    addMessage(
      "assistant",
      `오류가 발생했습니다: ${error.message}`
    );
  } finally {
    loadingIndicator.classList.add("hidden");
  }
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = chatInput.value.trim();

  if (!message) {
    return;
  }

  addMessage("user", message);

  chatInput.value = "";
  chatInput.focus();

  await sendChat(message);
});

refreshSummaryBtn.addEventListener("click", loadSummary);

loadSummary();