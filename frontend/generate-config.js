const fs = require("fs");

const apiBaseUrl =
  process.env.API_BASE_URL ||
  "https://gametrend-ai-api.onrender.com";

const content = `window.API_BASE_URL = "${apiBaseUrl}";\n`;

fs.writeFileSync("js/config.js", content);

console.log("Generated frontend/js/config.js");