const cityInput = document.getElementById("city-input");
const suggestionBox = document.getElementById("city-suggestions");

let cities = [];

fetch("/cities")
  .then(res => res.json())
  .then(data => {
    cities = data;
  });

cityInput.addEventListener("input", () => {
  const value = cityInput.value.toLowerCase();
  suggestionBox.innerHTML = "";

  if (!value) return;

  const matches = cities.filter(city =>
    city.toLowerCase().includes(value)
  ).slice(0, 8);

  matches.forEach(city => {
    const div = document.createElement("div");
    div.className = "suggestion-item";
    div.innerText = city;
    div.onclick = () => {
      cityInput.value = city;
      suggestionBox.innerHTML = "";
    };
    suggestionBox.appendChild(div);
  });
});

document.addEventListener("click", e => {
  if (!e.target.closest(".autocomplete")) {
    suggestionBox.innerHTML = "";
  }
});
