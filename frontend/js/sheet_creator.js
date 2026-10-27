const params = new URLSearchParams(window.location.search);
let sheet_id = params.get("sheet_id");

if (sheet_id === null) {
  sheet_id = "new";
}

console.log("Current sheet ID:", sheet_id);
let user;

game_system = document.getElementById("sheet_type");
dnd_sheet = document.getElementById("DnD_sheet");
// cyberpunk_sheet = document.getElementById("cyberpunk_sheet");
// pathfinder_sheet = document.getElementById("pathfinder_sheet");

let current_sheet;
save_button = document.getElementById("save");
skills_list = document.getElementById("skills_list");
skills = skills_list.querySelectorAll("button.skill");
skills.forEach(create_skill);

console.log("Connected to script file");

function hide_sheet() {
  dnd_sheet.style.display = "none";
  // cyberpunk_sheet.style.display = "none";
  // pathfinder_sheet.style.display = "none";
}

function set_sheet(event) {
  if (game_system.value == "DnD") {
    dnd_sheet.style.display = "block";
    current_sheet = dnd_sheet;
  }
  if (game_system.value == "Null") {
    hide_sheet();
    current_sheet = "No sheet";
  }
  /*
  * if (game_system.value == "Cyberpunk") {
  *   cyberpunk_sheet.style.display = "block";
  * }
  * if (game_system.value == "Pathfinders") {
  *   pathfinder_sheet.style.display = "block";
  * }
  */
}

function create_skill(skill) {
  skill.addEventListener("click", () => {
    event.preventDefault();
    let currentStage = parseInt(skill.dataset.stage, 10) || 0;
    let nextStage = (currentStage + 1) % 3;
    setSkillStage(skill, nextStage);
  });
}

function setSkillStage(skill, stage) {
  skill.dataset.stage = stage;
}

async function save_sheet() {
  let sheet_name = document.getElementById("name").value;
  let sheet_type = game_system.value;
  let form = current_sheet;
  let formData = new FormData(form);
  let data = Object.fromEntries(formData);
  let profData = {};

  form.querySelectorAll(".skill").forEach(button => {
    profData[button.name] = button.dataset.stage;
  });

  const packet = {
    sheet_id : sheet_id,
    user_id: user,
    name: sheet_name,
    type: sheet_type,
    basic_stats: data,
    skill_stats: profData
  };

  const response = await fetch("http://localhost:5000/save_sheet", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(packet)
  })
  .then(response => {
      console.log("status:", response.status);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      return response.json();
  })
  .then(data => {
      console.log("Saved", data);
      sheet_id = data.sheet_id;
  })
  .catch(error => {
      console.error("Failed:", error);
  });
}


game_system.addEventListener("change", set_sheet);
save.addEventListener("click", () => {
  if (!document.getElementById("required").reportValidity()) {
    return;
  }
  save_sheet();
});

document.addEventListener("DOMContentLoaded", () => {
  if (sheet_id !== "new") {
    requestSheet(sheet_id);
  }
});

async function requestSheet(sheet_id) {
  try {
    const response = await fetch(
      `http://localhost:5000/get_sheet/${encodeURIComponent(sheet_id)}`,
      {
        method: "GET",
        credentials: "include"
      }
    );

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || `HTTP ${response.status}`);
    }

    populateSheet(result.sheet);
  }
  catch (error) {
    console.error("Failed to load sheet:", error);
  }
}

function populateSheet(sheet) {
  sheet_id = sheet.sheet_id;

  const savedData = sheet.data;
  const textInputs = savedData.basic_stats || {};
  const buttonStates = savedData.skill_stats || {};

  document.getElementById("name").value = savedData.name;
  document.getElementById("sheet_type").value = savedData.type;

  for (const [inputName, value] of Object.entries(textInputs)) {
    const input = document.querySelector(
      `[name="${CSS.escape(inputName)}"]`
    );
    
    if (input) {
      input.value = value;
    }
  }

  for (const [buttonName, stage] of Object.entries(buttonStates)) {
    const button = document.querySelector(
      `[name="${CSS.escape(buttonName)}"]`
    );

    if (button) {
      setSkillStage(button, stage);
    }
  }
  set_sheet();
}

window.onload = set_sheet;
