var profileList = ["../static/images/girl-carousel.png", "../static/images/cat-carousel.png", "../static/images/bear-carousel.png",
    "../static/images/cockatoo-carousel.png", "../static/images/dog-carousel.png", "../static/images/gorilla-carousel.png",
    "../static/images/panda-carousel.png", "../static/images/rabbit-carousel.png"];

const carouselInner = document.getElementById('carouselInner');

// Loop through the image data and create carousel items
profileList.forEach((imageUrl, index) => {
    const carouselItem = document.createElement('div');
    carouselItem.classList.add('carousel-item');

    const img = document.createElement('img');
    img.src = imageUrl;
    img.classList.add('d-block');
    img.alt = `User ${index + 2}`;

    carouselItem.appendChild(img);
    carouselInner.appendChild(carouselItem);
});

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

function toggle(id) {
    var graphsDiv = document.getElementById('graphs')
    var tablesDiv = document.getElementById('tables')

    if (id === 'graphs') {
        graphsDiv.style.display = 'block'
        tablesDiv.style.display = 'none'
    } else if (id === 'tables') {
        tablesDiv.style.display = 'block'
        graphsDiv.style.display = 'none'
    }
}

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
