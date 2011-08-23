var myMessages = ['info','warning','error','success'];

function hideAllMessages() {
    var messagesHeights = new Array(); // this array will store height for each

    for (i=0; i<myMessages.length; i++) {
        messagesHeights[i] = $('.' + myMessages[i]).outerHeight(); // fill array
        $('.' + myMessages[i]).css('bottom', -messagesHeights[i]); //move element outside viewport
    }
}

function showMessage(type) {
    hideAllMessages();
    $('.'+type).animate({bottom:"0"}, 500).delay(500).queue(hideAllMessages());
}

$(document).ready(function() {
    // Initially, hide them all
    hideAllMessages();

    // When message is clicked, hide it
    $('.message').click(function() {
        $(this).animate({bottom: -$(this).outerHeight()}, 500);
    });
});
