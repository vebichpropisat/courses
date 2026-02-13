document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll('.rating .bi-star');
    const ratingForm = document.querySelector('form[name="rating"]');
    const ratingUrl = ratingForm ? ratingForm.dataset.url : null;
    let selectedRating = 0;
    let avgRating = parseFloat(document.getElementById("avg_rating").textContent) || 0;

    function highlightStars(value) {
        stars.forEach((star, index) => {
            if (index < value) {
                star.classList.add('bi-star-fill', 'text-warning');
                star.classList.remove('bi-star');
            } else {
                star.classList.add('bi-star');
                star.classList.remove('bi-star-fill', 'text-warning');
            }
        });
    }

    highlightStars(Math.round(avgRating));

    stars.forEach((star, index) => {
        star.addEventListener("mouseover", function () {
            highlightStars(index + 1);
        });

        star.addEventListener("mouseout", function () {
            highlightStars(selectedRating || Math.round(avgRating));
        });

        star.addEventListener("click", function () {
            selectedRating = index + 1;
            let courseId = document.querySelector('input[name="course"]').value;
            let csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

            fetch(ratingUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `course=${courseId}&star=${selectedRating}`
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById("avg_rating").textContent = data.avg_rating;
                        avgRating = data.avg_rating;
                        selectedRating = 0;
                        highlightStars(Math.round(avgRating));
                        alert("Рейтинг збережено!");
                    } else {
                        alert("Помилка!");
                                                            }
                })
                .catch(error => console.error("Помилка:", error));
        });
    });
});