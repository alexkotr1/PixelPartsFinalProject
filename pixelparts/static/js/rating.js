document.addEventListener('DOMContentLoaded', function () {
    const box = document.querySelector('.rating-input');
    if (!box) return;

    const stars = box.querySelectorAll('.star');
    const productId = box.dataset.productId;
    let userRating = parseInt(box.dataset.userRating) || 0;

    function paint(value) {
        stars.forEach(function (star) {
            const v = parseInt(star.dataset.value);
            star.classList.remove('bi-star-fill', 'bi-star');
            if (v <= value) {
                star.classList.add('bi-star-fill');
            } else {
                star.classList.add('bi-star');
            }
        });
    }

    paint(userRating);

    stars.forEach(function (star) {
        star.addEventListener('click', function () {
            const value = parseInt(star.dataset.value);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const formData = new FormData();
            formData.append('rating', value);
            formData.append('csrfmiddlewaretoken', csrfToken);

            fetch('/product/' + productId + '/rate/', {
                method: 'POST',
                body: formData,
            })
                .then(function (response) { return response.json(); })
                .then(function (data) {
                    userRating = data.user_rating;
                    paint(userRating);
                    console.log(data);
                    document.querySelector('.rating-average').textContent = data.average;
                    document.querySelector('.rating-count').textContent = data.count + (data.count === 1 ? ' rating' : ' ratings');
                });
        });
    });
});