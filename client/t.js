host = 'http://10.105.41.230:6560/'

$(function() {
    $.ajax({
        url: host + 'floors?building=教1',
    }).done(function(data) {
        console.log(data);
    }).fail(function(a, b, c) {
        console.log(a);
        console.log(b);
        console.log(c);
    });
});
