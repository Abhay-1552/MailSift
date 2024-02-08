function generate(data) {
    var dataValue = data;

    if (dataValue) {
        document.getElementById("zero-data-div").style.display = "none";
        document.getElementById("chart-divs").style.display = "block";
    } else {
        document.getElementById("zero-data-div").style.display = "block";
        document.getElementById("chart-divs").style.display = "none";
    }
    return true;
}

function showContent(option, element) {
    $('.option-content').hide();
    $('.nav-link').removeClass('active');
    $(element).addClass('active');
    $('#option' + (['Option 1', 'Option 2', 'Option 3', 'Option 4'].indexOf(option) + 1) + '-content').show();
}

// Filter Mail data into Table
function filterMail() {
    var keywords = document.getElementById("keywords").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/filter_mail", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            document.getElementById("resultContainer").innerHTML = response.result_table;
        }
    };
    xhr.send("keywords=" + keywords);
}
