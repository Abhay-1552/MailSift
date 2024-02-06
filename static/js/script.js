function showContent(option) {
    // Hide all option contents
    document.querySelectorAll('.option-content').forEach(function (el) {
        el.style.display = 'none';
    });

    // Show the selected option content
    document.getElementById(`option${getOptionNumber(option)}-content`).style.display = 'block';
}

function getOptionNumber(option) {
    // Extract the number from the option text
    return option.match(/\d+/)[0];
}

function generate(data) {
    var dataValue = data;

    if (dataValue == 0) {
        document.getElementById("zero-data-div").style.display = "block";
        document.getElementById("chart-divs").style.display = "none";
    } else {
        document.getElementById("zero-data-div").style.display = "none";
        document.getElementById("chart-divs").style.display = "block";
    }
    return true;
}