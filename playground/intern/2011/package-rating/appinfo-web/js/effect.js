// Rating
function initRating() {
    $('.rating').raty({
        hintList: ['', '', '', '', ''],
        half: true,
        start: score,
        click: raty_click
    });
}

// Message
function hideMessage() {
    messageHeight = $('.message').outerHeight(); // fill array
    $('.message').css('bottom', -messageHeight); //move element outside viewport
}

function showMessage(type, message) {
    messageHeight = $('.message').outerHeight(); // fill array
    hideMessage();
    $('.message').addClass(type).text(message).animate({bottom:"0"}, 500);
    // Hide message after 5s
    setTimeout(function() {
        $('.message').animate({bottom: -messageHeight}).removeClass(type).text('');
    }, 5000);
}

$(document).ready(function() {
    // Initially, hide the message
    hideMessage();

    // Show rating
    initRating();

    // When message is clicked, hide it
    $('.message').click(function() {
        $(this).animate({bottom: -$(this).outerHeight()}, 500);
    });
});
