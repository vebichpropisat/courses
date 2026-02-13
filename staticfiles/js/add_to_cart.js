document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.add-to-cart-form').forEach(function (form) {
        form.addEventListener('submit', function (event) {
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
                .then(response => {
                    return response.json()
                        .then(data => ({
                            status: response.status,
                            ok: response.ok,
                            data: data
                        }))
                        .catch(() => ({
                            status: response.status,
                            ok: response.ok,
                            data: { message: "Не вдалося розпізнати відповідь сервера." }
                        }));
                })
                .then(({ status, data }) => {
                    if (status === 200 && data.success) {
                        alert(data.message || 'Курс додано в кошик');
                    } else if (status === 401) {
                        alert(data.message || 'Потрібно авторизуватись');
                    } else if (status === 400) {
                        alert(data.message || 'Курс уже в кошику або вже куплений');
                    } else {
                        alert(data.message || 'Невідома помилка');
                    }
                })
                .catch(error => {
                    console.error("Fetch error:", error);
                    alert("Сталася помилка під час запиту");
                });
        });
    });
});


