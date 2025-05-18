// Smooth scroll behavior
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

// Parallax effect for hero section
window.addEventListener('scroll', function() {
    const parallax = document.querySelector('.hero-section');
    let scrollPosition = window.pageYOffset;
    parallax.style.transform = 'translateY(' + scrollPosition * 0.5 + 'px)';
});

// Animate elements on scroll
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach((element) => {
    observer.observe(element);
});

// Interactive map hover effects
document.querySelectorAll('.map-point').forEach(point => {
    point.addEventListener('mouseenter', function() {
        this.classList.add('active');
    });
    
    point.addEventListener('mouseleave', function() {
        this.classList.remove('active');
    });
});

// Dynamic loading animation
function showLoading() {
    const loader = document.createElement('div');
    loader.className = 'loader';
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.querySelector('.loader');
    if (loader) {
        loader.remove();
    }
}

// Smooth transitions between pages
document.addEventListener('click', function(e) {
    if (e.target.matches('.nav-link')) {
        e.preventDefault();
        const target = e.target.getAttribute('href');
        document.body.classList.add('page-transition');
        setTimeout(() => {
            window.location.href = target;
        }, 500);
    }
}); 