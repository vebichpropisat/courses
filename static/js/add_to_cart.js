document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.add-to-cart-form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(form);
            const csrfToken = formData.get('csrfmiddlewaretoken');

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Курс додано в кошик');
                } else {
                    alert('Курс наявний в кошику або вже куплений');
                }
            })
            .catch(error => {
                alert('Помилка');
                console.error(error);
            });
        });
    });
});