// Mobile Menu Toggle
const menuIcon = document.querySelector('.mobile-menu');
const navLinks = document.querySelector('.nav-links');

menuIcon.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    menuIcon.classList.toggle('active');
});

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
});

// Form Submission
const contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    // Add your form submission logic here
    alert('Thank you for your message! We will get back to you soon.');
    contactForm.reset();
});

// Scroll Animation for Feature Cards
const cards = document.querySelectorAll('.feature-card');
const observer = new IntersectionObserver(
    (entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    },
    { threshold: 0.1 }
);

cards.forEach(card => observer.observe(card));

// Stats Counter Animation
const stats = document.querySelectorAll('.stat h3');
let animated = false;

function animateStats() {
    if (animated) return;
    
    stats.forEach(stat => {
        const target = parseInt(stat.innerText);
        let count = 0;
        const duration = 2000; // 2 seconds
        const increment = target / (duration / 16); // 60fps

        const updateCount = () => {
            if (count < target) {
                count += increment;
                stat.innerText = Math.round(count);
                requestAnimationFrame(updateCount);
            } else {
                stat.innerText = target;
            }
        };

        updateCount();
    });
    
    animated = true;
}

// Trigger stats animation when mission section is in view
const missionSection = document.querySelector('.mission');
const statsObserver = new IntersectionObserver(
    (entries) => {
        if (entries[0].isIntersecting) {
            animateStats();
        }
    },
    { threshold: 0.5 }
);

statsObserver.observe(missionSection);