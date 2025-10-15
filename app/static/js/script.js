var myModal = document.getElementById("staticBackdrop");

myModal.addEventListener("shown.bs.modal", function () {
  // Get a list of all questions (table rows) on the page.
  let questions = Array.from(document.querySelectorAll("tbody tr"));
  // Get a list of all input fields in the modal.
  let modalFields = Array.from(myModal.querySelectorAll("input"));

  // For each input field in the modal, get the corresponding question and set the input field's value to the question's data-pq attribute value.
  for (let i = 0; i < modalFields.length; i++) {
    let question = questions[i].getAttribute("data-pq");
    modalFields[i].value = question ? question : "";
  }
});

document.getElementById("updateButton").addEventListener("click", function () {
  // Get a list of all input fields in the modal.
  let modalFields = Array.from(myModal.querySelectorAll("input"));
  // Map the input fields to their current values.
  let newQuestions = modalFields.map((field) => field.value);

  // Make a POST request to the /edit endpoint with the new questions.
  fetch("/edit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      paraphrases: newQuestions,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        location.reload();
      } else {
        console.error("Failed to update questions");
      }
    });
});
