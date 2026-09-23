const dataForm = document.getElementById("dataForm");
const dataDate = document.getElementById("dataDate");
const dataValue = document.getElementById("dataValue");
const dataMemo = document.getElementById("dataMemo");

const dataTableBody = document.getElementById("dataTableBody");
const dataStatus = document.getElementById("dataStatus");
const refreshDataBtn = document.getElementById("refreshDataBtn");

const dataSearch = document.getElementById("dataSearch");
const dataCountInfo = document.getElementById("dataCountInfo");

const prevPageBtn = document.getElementById("prevPageBtn");
const nextPageBtn = document.getElementById("nextPageBtn");
const pageInfo = document.getElementById("pageInfo");


let allData = [];
let filteredData = [];

let currentPage = 1;
const pageSize = 10;


function setDataStatus(message, isError = false) {
  dataStatus.textContent = message;

  dataStatus.className = isError
    ? "data-status error"
    : "data-status success";
}


function createDataRow(item) {
  const row = document.createElement("tr");

  const dateCell = document.createElement("td");
  dateCell.textContent = item.date;

  const valueCell = document.createElement("td");
  valueCell.textContent =
    Number(item.value).toLocaleString("ko-KR");

  const memoCell = document.createElement("td");
  memoCell.textContent = item.memo || "-";

  const actionCell = document.createElement("td");

  const deleteButton = document.createElement("button");

  deleteButton.type = "button";
  deleteButton.className = "delete-button";
  deleteButton.textContent = "삭제";

  deleteButton.addEventListener("click", async () => {
    const confirmed = confirm(
      `${item.date} 데이터를 삭제할까요?`
    );

    if (!confirmed) {
      return;
    }

    try {
      await apiRequest(`/api/data/${item.id}`, {
        method: "DELETE",
      });

      setDataStatus("데이터가 삭제되었습니다.");

      await loadData();
      await loadSummary();

    } catch (error) {
      setDataStatus(
        `삭제 실패: ${error.message}`,
        true
      );
    }
  });

  actionCell.appendChild(deleteButton);

  row.appendChild(dateCell);
  row.appendChild(valueCell);
  row.appendChild(memoCell);
  row.appendChild(actionCell);

  return row;
}


function renderDataPage() {
  dataTableBody.innerHTML = "";

  const totalPages =
    Math.max(
      1,
      Math.ceil(filteredData.length / pageSize)
    );

  if (currentPage > totalPages) {
    currentPage = totalPages;
  }

  const start =
    (currentPage - 1) * pageSize;

  const end =
    start + pageSize;

  const pageItems =
    filteredData.slice(start, end);

  if (pageItems.length === 0) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");

    cell.colSpan = 4;
    cell.className = "empty-row";
    cell.textContent = "표시할 데이터가 없습니다.";

    row.appendChild(cell);
    dataTableBody.appendChild(row);

  } else {
    pageItems.forEach((item) => {
      dataTableBody.appendChild(
        createDataRow(item)
      );
    });
  }

  pageInfo.textContent =
    `${currentPage} / ${totalPages}`;

  dataCountInfo.textContent =
    `총 ${filteredData.length}개`;

  prevPageBtn.disabled =
    currentPage <= 1;

  nextPageBtn.disabled =
    currentPage >= totalPages;
}


function applyDataFilter() {
  const keyword =
    dataSearch.value
      .trim()
      .toLowerCase();

  filteredData =
    allData.filter((item) => {
      const date =
        item.date?.toLowerCase() || "";

      const memo =
        item.memo?.toLowerCase() || "";

      return (
        date.includes(keyword) ||
        memo.includes(keyword)
      );
    });

  currentPage = 1;

  renderDataPage();
}


async function loadData() {
  try {
    const dataList =
      await apiRequest("/api/data");

    allData = [...dataList].sort(
      (a, b) =>
        b.date.localeCompare(a.date)
    );

    filteredData = [...allData];

    currentPage = 1;

    renderDataPage();

  } catch (error) {
    setDataStatus(
      `데이터 조회 실패: ${error.message}`,
      true
    );
  }
}


dataForm.addEventListener(
  "submit",
  async (event) => {

    event.preventDefault();

    const payload = {
      date: dataDate.value,
      value: Number(dataValue.value),
      memo: dataMemo.value.trim(),
    };

    try {
      await apiRequest("/api/data", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      setDataStatus(
        "데이터가 추가되었습니다."
      );

      dataForm.reset();

      await loadData();
      await loadSummary();

    } catch (error) {
      setDataStatus(
        `추가 실패: ${error.message}`,
        true
      );
    }
  }
);


refreshDataBtn.addEventListener(
  "click",
  loadData
);


dataSearch.addEventListener(
  "input",
  applyDataFilter
);


prevPageBtn.addEventListener(
  "click",
  () => {
    if (currentPage > 1) {
      currentPage--;
      renderDataPage();
    }
  }
);


nextPageBtn.addEventListener(
  "click",
  () => {
    const totalPages =
      Math.ceil(
        filteredData.length / pageSize
      );

    if (currentPage < totalPages) {
      currentPage++;
      renderDataPage();
    }
  }
);


loadData();

const downloadCsvBtn = document.getElementById("downloadCsvBtn");

function escapeCsvValue(value) {
  const text = String(value ?? "");

  if (
    text.includes(",") ||
    text.includes('"') ||
    text.includes("\n")
  ) {
    return `"${text.replace(/"/g, '""')}"`;
  }

  return text;
}

async function downloadCsv() {
  try {
    const data = await apiRequest("/api/data");

    const rows = [
      ["date", "value", "memo"],
      ...data.map((item) => [
        item.date,
        item.value,
        item.memo ?? "",
      ]),
    ];

    const csvContent = rows
      .map((row) =>
        row.map(escapeCsvValue).join(",")
      )
      .join("\n");

    const blob = new Blob(
      ["\uFEFF" + csvContent],
      {
        type: "text/csv;charset=utf-8;",
      }
    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "gametrend_data.csv";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  } catch (error) {
    console.error("CSV 다운로드 실패:", error);
    alert("CSV 다운로드 중 오류가 발생했습니다.");
  }
}

if (downloadCsvBtn) {
  downloadCsvBtn.addEventListener(
    "click",
    downloadCsv
  );
}