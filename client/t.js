$(function() {
    $.ajax({
        url: 'http://fans656.pythonanywhere.com/buildings',
    }).done(function(data) {
        console.log(data);
    });
});
