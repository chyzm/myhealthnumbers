window.alert('Smash that fitness goal')

// JavaScript to show the button when scrolling down and scroll to top on click
document.addEventListener('scroll', function() {
    var scrollPosition = window.scrollY;
    var backToTopButton = document.getElementById('back-to-top');
    
    if (scrollPosition > 200) {
        backToTopButton.classList.add('show');
    } else {
        backToTopButton.classList.remove('show');
    }
});

// Scroll to top function
document.getElementById('back-to-top').addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

