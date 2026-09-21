const API_BASE_URL = "https://gametrend-ai-api.onrender.com";

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json();

  if (!response.ok) {
    const message =
      data.detail ||
      data.message ||
      "API 요청 중 오류가 발생했습니다.";

    throw new Error(message);
  }

  return data;
}