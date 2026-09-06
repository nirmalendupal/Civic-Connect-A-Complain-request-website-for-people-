// =============================
// SEARCH + CATEGORY FILTER
// =============================

const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const problemCards = document.querySelectorAll(".problem-card");

function filterProblems() {

    const searchText = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;

    problemCards.forEach(card => {

        const text = card.innerText.toLowerCase();
        const category = card.dataset.category;

        const matchesSearch = text.includes(searchText);

        const matchesCategory =
            selectedCategory === "all" ||
            category === selectedCategory;

                if (matchesSearch && matchesCategory) {
            card.style.display = "block";
            card.classList.remove("card-hidden");
            card.classList.add("card-show");
        } else {
            card.classList.remove("card-show");
            card.classList.add("card-hidden");
        
            setTimeout(() => {
                card.style.display = "none";
            }, 300);
        }

    });
}

searchInput.addEventListener("input", filterProblems);
categoryFilter.addEventListener("change", filterProblems);


// =============================
// UPVOTE BUTTON
// =============================

const upvoteButtons = document.querySelectorAll(".upvote");

upvoteButtons.forEach(button => {

    button.addEventListener("click", () => {

        const count = button.querySelector("span");

        let currentCount = parseInt(count.innerText);

        currentCount++;

        count.innerText = currentCount;

        button.innerHTML = `❤️ <span>${currentCount}</span>`;

    });

});


// =============================
// IMAGE PREVIEW
// =============================

const imageInput = document.getElementById("problemImage");
const imagePreview = document.getElementById("imagePreview");

imageInput.addEventListener("change", () => {

    const file = imageInput.files[0];

    if (!file) {
        imagePreview.innerHTML = "";
        return;
    }

    const imageURL = URL.createObjectURL(file);

    imagePreview.innerHTML = `
        <img src="${imageURL}" alt="Problem image">
    `;

});


