$('input[type="checkbox"]').on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    return false;
});