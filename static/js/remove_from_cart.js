document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.remove-from-cart-form').forEach(function(form) {
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
                    alert(data.message);
                    const card = form.closest('.card');
                    const price = parseFloat(card.querySelector('.card-text strong').textContent.replace('$', '').replace(',', '.')) || 0;

                    card.remove();

                    const totalPriceElement = document.querySelector("#total_price");
                    let totalPrice = parseFloat(totalPriceElement.textContent.replace('$', '').replace(',', '.')) || 0;
                    totalPrice -= price;
                    totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
                } else {
                    alert('Помилка при видаленні курса');
                }
            })
            .catch(error => {
                alert('Помилка');
                console.error(error);
            });
        });
    });
});
