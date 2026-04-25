document.addEventListener('DOMContentLoaded', function () {
    const box = document.querySelector('.rating-input');
    if (!box) return;

    const stars = box.querySelectorAll('.star');
    const productId = box.dataset.productId; //set via data-product-id attribute
    let userRating = parseInt(box.dataset.userRating) || 0; // 0 if user hasnt rated

    //function to fill starts till it hits the value and unfill the rest
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

    paint(userRating); //fill users existing rating on page load

    stars.forEach(function (star) {
        star.addEventListener('click', function () {
            const value = parseInt(star.dataset.value);
            //scrape the csrf token from the hidden <form>{% csfr token%}</form> in rating.html
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
                    //update the stars and the average rating without reloading the page
                    userRating = data.user_rating;
                    paint(userRating);
                    document.querySelector('.rating-average').textContent = data.average;
                    document.querySelector('.rating-count').textContent = data.count + (data.count === 1 ? ' rating' : ' ratings');
                });
        });
    });
});