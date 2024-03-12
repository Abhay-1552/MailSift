function filterDivs() {
    var input, filter, cards, card, cardContent, i, txtValue;
    input = document.getElementById('searchInput');
    filter = input.value.toUpperCase();
    cards = document.querySelectorAll('.section[name="middle-section"] .card'); // Select cards only within the middle section

    // Loop through all cards, and hide those who don't match the search query
    cards.forEach(function (card) {
        cardContent = card.querySelector('.card-header').textContent + card.querySelector('.card-body').textContent;
        txtValue = cardContent.toUpperCase();
        if (txtValue.indexOf(filter) > -1) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    });
}

// Bind the filterDivs function to the input's 'input' event
document.getElementById('searchInput').addEventListener('input', filterDivs);

// Update the mail count
document.addEventListener("DOMContentLoaded", function () {
    var count = document.querySelectorAll('.section[name="middle-section"] .card').length;
    document.getElementById('mailcount').textContent = count;
});

// Show details of the clicked card
var cards = document.querySelectorAll('.scrollable-section .card');
var blankCard = document.getElementById('blankCard');

// Add click event listener to each card
cards.forEach(function (card) {
    card.addEventListener('click', function () {
        // Extract information from the clicked card
        var senderName = this.querySelector('#sendername').textContent;
        var senderEmail = this.querySelector('#sendermail').textContent;
        var subject = this.querySelector('#subject').textContent;
        var body = this.querySelector('#payload').textContent;

        // Populate information into the blank card
        document.getElementById('blankSenderName').textContent = senderName;
        document.getElementById('blankSenderEmail').textContent = senderEmail;
        document.getElementById('blankSubject').textContent = subject;
        document.getElementById('blankPayload').textContent = body;
    });
});