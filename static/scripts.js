document.addEventListener('DOMContentLoaded', function () {
    const titleElement = document.getElementById('editable-title');
    const titleForm = document.getElementById('title-form');
    
    const locationElement = document.getElementById('editable-location');
    const timeElement = document.getElementById('editable-time');
    const detailsForm = document.getElementById('details-form');

    function handleEditClick(element, form) {
        element.addEventListener('click', function () {
            element.style.display = 'none'; // Hide the text
            form.style.display = 'block';  // Show the form
            form.elements[0].focus(); // Focus on the input field
        });
    }

    function handleFormSubmit(form, textElement) {
        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent default form submission

            const formData = new FormData(form);
            const newText = formData.get(form.elements[0].name);

            // Update text on the page
            textElement.textContent = newText;
            textElement.style.display = 'block';
            form.style.display = 'none';

            // Submit the form to update on the server
            fetch(form.action, {
                method: 'POST',
                body: new URLSearchParams(new FormData(form)),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
        });
    }

    // Title editing
    handleEditClick(titleElement, titleForm);
    handleFormSubmit(titleForm, titleElement);

    // Event details editing
    handleEditClick(locationElement, detailsForm);
    handleEditClick(timeElement, detailsForm);
    handleFormSubmit(detailsForm, locationElement); // Use locationElement for simplicity; same form for both fields
});
