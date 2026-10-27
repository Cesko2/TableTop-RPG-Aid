/*
 * dashboard.js
 * This will be the script file for our dashboard page. The purpose of this file is to provide all scripting needs,
 * namely it will forward data to the backend using api requests so that the backend still handles the brunt of the work.
 * That being said it will also contain any and all scripts that need not be delegated to the backend, but need be done anyhow, such as page navigation.
 */
const button = document.getElementById("create_character");

function swap_screen() {
  
  window.location.href = "sheet_creator.html";
}

document.addEventListener("DOMContentLoaded", loadSheets);

async function loadSheets() {
  const sheetList = document.querySelector("#characters");

  try {
    const response = await fetch("http://localhost:5000/get_sheets", {
      method:"GET",
      credentials: "include"
    });
    const result = await response.json();

    if (!response.ok) {
      throw new Error(
        result.message || `HTTP ${response.status}`
      );
    }

    displaySheets(result.sheets);
  }

  catch (error) {
    console.error("failed to load sheets:", error);

    sheetList.replaceChildren();
    const message = document.createElement("p");
    message.textContent = "Unable to load your sheets.";
    sheetList.appendChild(message);
  }
}

function displaySheets(sheets) {
  const sheetList = document.querySelector("#character-list");

  sheetList.replaceChildren();

  if (sheets.length === 0) {
    const message = document.createElement("p");
    message.textContent = "You have not created any sheets yet.";

    sheetList.appendChild(message);
    return;
  }

  for (const sheet of sheets) {
    const button = createSheetButton(sheet);
    sheetList.appendChild(button);
  }
}

function createSheetButton(sheet) {
  const button = document.createElement("button");

  button.type = "button";
  button.classList.add("character-card")

  const name = document.createElement("h3");
  name.textContent = sheet.name;

  const details = document.createElement("p");
  details.textContent = `Level ${sheet.level} - ${sheet.character_class}`;

  const type = document.createElement("p");
  type.textContent = `Game System: ${sheet.sheet_type}`;

  button.appendChild(name);
  button.appendChild(details);
  button.appendChild(type);

  button.addEventListener("click", () => {
    const encodedId = encodeURIComponent(sheet.sheet_id);

    window.location.href = `sheet_creator.html?sheet_id=${encodedId}`;
  });

  return button;
}

button.addEventListener("click", swap_screen);
