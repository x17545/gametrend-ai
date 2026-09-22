const conversationList =
  document.getElementById("conversationList");

const refreshConversationsBtn =
  document.getElementById("refreshConversationsBtn");


function formatConversationDate(value) {
  if (!value) {
    return "";
  }

  const date = new Date(value);

  return date.toLocaleString("ko-KR");
}


function renderConversation(conversation) {
  const item = document.createElement("div");
  item.className = "conversation-item";

  const info = document.createElement("button");
  info.type = "button";
  info.className = "conversation-open";

  const title = document.createElement("strong");
  title.textContent =
    conversation.title || "제목 없는 대화";

  const date = document.createElement("span");
  date.textContent =
    formatConversationDate(conversation.created_at);

  info.appendChild(title);
  info.appendChild(date);

  info.addEventListener("click", async () => {
    try {
      const result = await apiRequest(
        `/api/conversations/${conversation.id}`
      );

      chatMessages.innerHTML = "";

      result.messages.forEach((message) => {
        addMessage(
          message.role,
          message.content
        );
      });

      chatMessages.scrollTop =
        chatMessages.scrollHeight;

      document
        .querySelector(".analyst-console")
        .scrollIntoView({
          behavior: "smooth",
          block: "start",
        });

    } catch (error) {
      alert(
        `대화 불러오기 실패: ${error.message}`
      );
    }
  });


  const deleteButton = document.createElement("button");

  deleteButton.type = "button";
  deleteButton.className = "conversation-delete";
  deleteButton.textContent = "삭제";

  deleteButton.addEventListener("click", async () => {
    const confirmed = confirm(
      `"${conversation.title}" 대화를 삭제할까요?`
    );

    if (!confirmed) {
      return;
    }

    try {
      await apiRequest(
        `/api/conversations/${conversation.id}`,
        {
          method: "DELETE",
        }
      );

      await loadConversations();
    } catch (error) {
      alert(
        `대화 삭제 실패: ${error.message}`
      );
    }
  });

  item.appendChild(info);
  item.appendChild(deleteButton);

  return item;
}


async function loadConversations() {
  try {
    const conversations =
      await apiRequest("/api/conversations");

    conversationList.innerHTML = "";

    if (conversations.length === 0) {
      const empty = document.createElement("p");

      empty.className = "conversation-empty";
      empty.textContent =
        "저장된 대화가 없습니다.";

      conversationList.appendChild(empty);

      return;
    }

    conversations.forEach((conversation) => {
      conversationList.appendChild(
        renderConversation(conversation)
      );
    });
  } catch (error) {
    conversationList.innerHTML =
      `<p class="conversation-empty">
        대화 목록을 불러오지 못했습니다.
      </p>`;

    console.error(error);
  }
}


refreshConversationsBtn.addEventListener(
  "click",
  loadConversations
);


loadConversations();