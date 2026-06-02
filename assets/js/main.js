// Moqeet Academy - Main JavaScript File
// WhatsApp: +923315162406

document.addEventListener('DOMContentLoaded', function() {

    // ===== MOBILE MENU TOGGLE =====
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');

            // Change icon between hamburger and close
            const icon = this.textContent;
            this.textContent = icon === '☰' ? '✕' : '☰';
        });

        // Close menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-menu a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                mobileMenuToggle.textContent = '☰';
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInsideNav = navMenu.contains(event.target);
            const isClickOnToggle = mobileMenuToggle.contains(event.target);

            if (!isClickInsideNav && !isClickOnToggle && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                mobileMenuToggle.textContent = '☰';
            }
        });
    }

    // ===== ENSURE ABOUT LINK IS AVAILABLE SITE-WIDE =====
    if (navMenu) {
        const aboutHref = '/about/';
        const hasAbout = Array.from(navMenu.querySelectorAll('a')).some(a => a.getAttribute('href') === aboutHref);
        if (!hasAbout) {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = aboutHref;
            a.textContent = 'About';
            li.appendChild(a);
            navMenu.appendChild(li);
        }
    }

    // ===== ACTIVE NAVIGATION LINK =====
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation ||
            (currentLocation.includes(link.getAttribute('href')) && link.getAttribute('href') !== '/')) {
            link.classList.add('active');
        }
    });

    // ===== SMOOTH SCROLL FOR ANCHOR LINKS =====
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');

            if (targetId !== '#' && targetId !== '') {
                e.preventDefault();
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    const headerOffset = 80;
                    const elementPosition = targetElement.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // ===== FLOATING WHATSAPP BUTTON =====
    // Create floating WhatsApp button if it doesn't exist
    if (!document.querySelector('.whatsapp-float')) {
        const whatsappFloat = document.createElement('a');
        whatsappFloat.href = 'https://wa.me/923315162406';
        whatsappFloat.className = 'whatsapp-float';
        whatsappFloat.target = '_blank';
        whatsappFloat.rel = 'noopener noreferrer';
        whatsappFloat.setAttribute('aria-label', 'Contact us on WhatsApp');
        whatsappFloat.innerHTML = '💬';
        document.body.appendChild(whatsappFloat);
    }

    // ===== SCROLL TO TOP FUNCTIONALITY =====
    let scrollTimeout;
    window.addEventListener('scroll', function() {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function() {
            const whatsappButton = document.querySelector('.whatsapp-float');
            if (whatsappButton) {
                if (window.pageYOffset > 300) {
                    whatsappButton.style.opacity = '1';
                    whatsappButton.style.visibility = 'visible';
                } else {
                    whatsappButton.style.opacity = '1';
                    whatsappButton.style.visibility = 'visible';
                }
            }
        }, 100);
    });

    // ===== LAZY LOADING FOR IMAGES =====
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // ===== FORM VALIDATION (if contact form exists) =====
    const contactForm = document.querySelector('#contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const name = this.querySelector('[name="name"]').value.trim();
            const email = this.querySelector('[name="email"]').value.trim();
            const message = this.querySelector('[name="message"]').value.trim();

            if (!name || !email || !message) {
                alert('Please fill in all fields');
                return;
            }

            if (!isValidEmail(email)) {
                alert('Please enter a valid email address');
                return;
            }

            // Redirect to WhatsApp with pre-filled message
            const whatsappMessage = `Name: ${name}%0AEmail: ${email}%0AMessage: ${message}`;
            window.open(`https://wa.me/923315162406?text=${whatsappMessage}`, '_blank');

            // Reset form
            this.reset();
        });
    }

    // ===== EMAIL VALIDATION HELPER =====
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // ===== ANIMATE ON SCROLL =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.subject-card, .step-item, .feature-item, .testimonial-card');

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // ===== STATS COUNTER ANIMATION =====
    const statNumbers = document.querySelectorAll('.stat-item h3');
    let hasAnimated = false;

    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;
                statNumbers.forEach(stat => {
                    const target = parseInt(stat.textContent);
                    animateCounter(stat, 0, target, 2000);
                });
            }
        });
    }, { threshold: 0.5 });

    const statsSection = document.querySelector('.stats-strip');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }

    function animateCounter(element, start, end, duration) {
        const range = end - start;
        const increment = range / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                element.textContent = end + '+';
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current) + '+';
            }
        }, 16);
    }

    // ===== CHAPTER LIST ACTIVE STATE =====
    const chapterLinks = document.querySelectorAll('.chapter-list a');
    const currentPath = window.location.pathname;

    chapterLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // ===== COPY TO CLIPBOARD FUNCTIONALITY =====
    const copyButtons = document.querySelectorAll('[data-copy]');

    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');

            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = this.textContent;
                this.textContent = 'Copied!';

                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        });
    });

    // ===== AUTO YEAR IN FOOTER =====
    document.querySelectorAll('.current-year').forEach(el => {
        if (!el.textContent.trim()) {
            el.textContent = new Date().getFullYear();
        }
    });

});

// ===== EXTERNAL LINK HANDLER =====
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A' && e.target.hostname !== window.location.hostname) {
        e.target.setAttribute('rel', 'noopener noreferrer');
    }
});

// ===== CONSOLE MESSAGE =====
console.log('%cMoqeet Academy', 'font-size: 24px; font-weight: bold; color: #1B4332;');
console.log('%cFree Class 9 & 10 Notes | NBF Syllabus Pakistan', 'font-size: 14px; color: #D4A017;');
console.log('%cWhatsApp: +923315162406', 'font-size: 12px; color: #25D366;');
