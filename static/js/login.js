function keyCheck(element, e) {
    if (e.key === 'Enter') {
        send(element);
    }
}

function send(element) {
    const formData = new FormData(element.parentElement);
    const request = new XMLHttpRequest();

    request.open('POST', '/login');
    request.send(formData);

    request.onreadystatechange = function () {
        if (request.readyState === XMLHttpRequest.DONE) {
            handleResponse(request, element); // Pasa el elemento al manejar la respuesta
        }
    };
}

function handleResponse(request, element) {
    if (request.status === 200) {
        try {
            const data = JSON.parse(request.responseText);
            if (data.success) {
                resetForm(element.parentElement);
                window.location.reload();
            } else {
                showError(element.parentElement);
            }
        } catch (error) {
            console.error('Error parsing JSON response:', error);
        }
    } else {
        console.error('Request failed with status:', request.status);
    }
}

function resetForm(formElement) {
    formElement.style = '';
}

function showError(formElement) {
    formElement.classList.add('error');
}

function pass_view() {
    const pass_view = document.getElementById("password_view");
    const pass_input = document.getElementById("password_input");

    pass_input.type = (pass_input.type === 'password') ? 'text' : 'password';
    pass_view.value = (pass_input.type === 'password') ? texts.show : texts.hide;
}