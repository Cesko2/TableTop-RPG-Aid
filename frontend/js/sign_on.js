/*
 * sign_on.js
 * The purpose of sign_on.js is to submit api requests to the backend, and provide any scrips necssary for page traversal.
 * It will serve as the middleman between the user and the server if you wish to think of it that way.
 */
const form = document.getElementById("sign_on_form")

async function attempt_sign_on(event) {
  event.preventDefault();
  
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const success = await submit_auth_request(username, password);

  if (success == true) {
    window.location.href = "dashboard.html";
  }

}

async function submit_auth_request(username, password) {
  /*
   * debug function currently, will be filled out later with proper functionality
   */
  const sign_on = {username, password};

  try {
    const response = await fetch("http://localhost:5000/login",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(sign_on)
    }
    );
    const data = await response.json();
    
    if (!response.ok) {
      console.error(data.message);
      return false;
    }

    console.log(`Authenticated user ${data.username}, ID ${data.user_id}`);
    return data.success;
  }

  catch (error) {
    console.error("Failed Connection", error);
    return false;
  }

  /*
  if (username == "debug" && password == "debug") {
    return true;
  }

  console.log("Failed sign_on");
  return false;
  */
}

form.addEventListener("submit", attempt_sign_on);
