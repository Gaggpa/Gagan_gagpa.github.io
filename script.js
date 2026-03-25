// Mobile Navigation Toggle
const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");

if (hamburger) {
    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("active");
        navLinks.classList.toggle("active");
    });
}

document.querySelectorAll(".nav-links a").forEach(n => n.addEventListener("click", () => {
    if (hamburger) {
        hamburger.classList.remove("active");
        navLinks.classList.remove("active");
    }
}));

// Navbar Scroll Effect
const navbar = document.getElementById("navbar");

if (navbar) {
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });
}

// Scroll Animations using Intersection Observer
const appearOptions = {
    threshold: 0.15,
    rootMargin: "0px 0px -50px 0px"
};

const appearOnScroll = new IntersectionObserver(function(entries, observer) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("appear");
        observer.unobserve(entry.target);
    });
}, appearOptions);

document.querySelectorAll(".fade-in, .fade-in-up, .fade-in-left, .fade-in-right").forEach(fader => {
    appearOnScroll.observe(fader);
});

// Active Menu State
const sections = document.querySelectorAll('section, header');
const navItems = document.querySelectorAll('.nav-links a');

if (navItems.length > 0) {
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - sectionHeight / 3)) {
                current = section.getAttribute('id');
            }
        });

        navItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href').includes(current)) {
                item.classList.add('active');
            }
        });
    });
}

// ============================
// PARTICLE BACKGROUND
// ============================
const canvas = document.getElementById('particles-canvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let particles = [];
    const PARTICLE_COUNT = 60;

    function resizeCanvas() {
        const hero = document.getElementById('hero');
        canvas.width = hero.offsetWidth;
        canvas.height = hero.offsetHeight;
    }

    class Particle {
        constructor() {
            this.reset();
        }
        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2.5 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.6;
            this.speedY = (Math.random() - 0.5) * 0.6;
            this.opacity = Math.random() * 0.5 + 0.1;
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
            if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
        }
        draw() {
            ctx.globalAlpha = this.opacity;
            ctx.fillStyle = '#6366f1';
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function initParticles() {
        particles = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            particles.push(new Particle());
        }
    }

    function drawConnections() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 120) {
                    ctx.globalAlpha = 0.08 * (1 - dist / 120);
                    ctx.strokeStyle = '#6366f1';
                    ctx.lineWidth = 0.5;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
    }

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        drawConnections();
        ctx.globalAlpha = 1;
        requestAnimationFrame(animateParticles);
    }

    resizeCanvas();
    initParticles();
    animateParticles();
    window.addEventListener('resize', () => {
        resizeCanvas();
        initParticles();
    });
}

// ============================
// 3D TILT EFFECT ON PROJECT CARDS
// ============================
document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -6;
        const rotateY = ((x - centerX) / centerX) * 6;
        card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) translateY(0)';
    });
});

// ============================
// TYPING ANIMATION FOR HERO
// ============================
const typedEl = document.getElementById('typed-name');
if (typedEl) {
    const text = typedEl.textContent;
    typedEl.textContent = '';
    typedEl.style.borderRight = '3px solid var(--primary-color)';
    let charIndex = 0;

    function typeChar() {
        if (charIndex < text.length) {
            typedEl.textContent += text.charAt(charIndex);
            charIndex++;
            setTimeout(typeChar, 100);
        } else {
            // Blinking cursor effect
            setInterval(() => {
                typedEl.style.borderRight = typedEl.style.borderRight === 'none' ? '3px solid var(--primary-color)' : 'none';
            }, 500);
        }
    }

// Start typing after a small delay
    setTimeout(typeChar, 800);
}

// ============================
// SPA GALLERY OVERLAY LOGIC
// ============================
const body = document.body;
let currentGalleryId = null;
let carouselIndexes = { 'sanosat': 0, 'decimalsat': 0, 'vegafly': 0 };

function openGallery(projectId) {
    const overlay = document.getElementById(`gallery-${projectId}`);
    if (!overlay) return;

    currentGalleryId = projectId;
    
    // Show overlay smoothly
    overlay.classList.add('active');
    
    // Prevent background scrolling
    body.style.overflow = 'hidden';
    
    // Initialize/Reset its corresponding 3D carousel
    updateGalleryCarousel(projectId, carouselIndexes[projectId]);
}

function closeGallery() {
    if (!currentGalleryId) return;
    
    const overlay = document.getElementById(`gallery-${currentGalleryId}`);
    if (overlay) {
        overlay.classList.remove('active');
    }
    
    // Restore scrolling
    body.style.overflow = '';
    currentGalleryId = null;
}

// 3D Carousel Logic per gallery
function updateGalleryCarousel(projectId, targetIndex) {
    if (!window.GALLERY_DATA || !window.GALLERY_DATA[projectId]) return;
    
    const totalSlides = window.GALLERY_DATA[projectId].length;
    // Handle wrap-around
    carouselIndexes[projectId] = ((targetIndex % totalSlides) + totalSlides) % totalSlides;
    const currentIndex = carouselIndexes[projectId];
    
    const slides = Array.from(document.querySelectorAll(`.${projectId}-slide`));
    const currentEl = document.getElementById(`${projectId}-current`);
    
    if (currentEl) currentEl.textContent = currentIndex + 1;

    slides.forEach((slide, index) => {
        let diff = index - currentIndex;
        
        // Shortest path calculation
        if (diff > totalSlides / 2) diff -= totalSlides;
        if (diff < -totalSlides / 2) diff += totalSlides;
        
        const absDiff = Math.abs(diff);
        const translateX = diff * 50; 
        const translateZ = absDiff * -200; 
        const rotateY = diff * -25; 
        
        slide.style.transform = `translateX(${translateX}%) translateZ(${translateZ}px) rotateY(${rotateY}deg)`;
        slide.style.zIndex = totalSlides - absDiff;
        
        const opacity = absDiff > 3 ? 0 : (1 - (absDiff * 0.2));
        slide.style.opacity = opacity > 0 ? opacity : 0;
        slide.style.filter = absDiff === 0 ? 'brightness(1)' : 'brightness(0.6)';
        
        if (absDiff === 0) slide.classList.add('center');
        else slide.classList.remove('center');
        
        if (absDiff > 3) slide.style.pointerEvents = 'none';
        else slide.style.pointerEvents = 'auto';
    });
}

// Attach event listeners for Carousels
['sanosat', 'decimalsat', 'vegafly'].forEach(pid => {
    const prevBtn = document.getElementById(`${pid}-prev`);
    const nextBtn = document.getElementById(`${pid}-next`);
    
    if (prevBtn) {
        prevBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            updateGalleryCarousel(pid, carouselIndexes[pid] - 1);
        });
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            updateGalleryCarousel(pid, carouselIndexes[pid] + 1);
        });
    }
    
    // Clicking individual slides
    const slides = Array.from(document.querySelectorAll(`.${pid}-slide`));
    slides.forEach((slide, idx) => {
        slide.addEventListener('click', () => {
            if (idx === carouselIndexes[pid]) {
                openLightbox(idx);
            } else {
                updateGalleryCarousel(pid, idx);
            }
        });
    });
    
    // Swipe support for carousel container
    const wrapper = document.getElementById(`${pid}-carousel-wrapper`);
    if (wrapper) {
        let touchStartX = 0;
        wrapper.addEventListener('touchstart', e => { touchStartX = e.changedTouches[0].screenX; }, {passive: true});
        wrapper.addEventListener('touchend', e => {
            const diff = touchStartX - e.changedTouches[0].screenX;
            if (Math.abs(diff) > 50) {
                if (diff > 0) updateGalleryCarousel(pid, carouselIndexes[pid] + 1);
                else updateGalleryCarousel(pid, carouselIndexes[pid] - 1);
            }
        });
    }
});

// ============================
// LIGHTBOX FULLSCREEN LOGIC
// ============================
const lightbox = document.getElementById('spa-lightbox');
const lbImg = document.getElementById('spa-lb-img');
const lbCurrent = document.getElementById('spa-lb-current');
const lbTotal = document.getElementById('spa-lb-total');
const lbClose = document.getElementById('spa-lb-close');
const lbPrev = document.getElementById('spa-lb-prev');
const lbNext = document.getElementById('spa-lb-next');

let lightboxIndex = 0;

function showLightboxImage(idx) {
    if (!currentGalleryId || !window.GALLERY_DATA[currentGalleryId]) return;
    
    const images = window.GALLERY_DATA[currentGalleryId];
    lightboxIndex = ((idx % images.length) + images.length) % images.length;
    
    lbTotal.textContent = images.length;
    lbImg.style.opacity = '0';
    
    setTimeout(() => {
        lbImg.src = images[lightboxIndex];
        lbImg.onload = () => { lbImg.style.opacity = '1'; };
        lbCurrent.textContent = lightboxIndex + 1;
        
        // Sync underlying carousel so when you close, it's at the same image
        updateGalleryCarousel(currentGalleryId, lightboxIndex);
    }, 150);
}

function openLightbox(idx) {
    if (!lightbox) return;
    lightbox.classList.add('active');
    showLightboxImage(idx);
}

function closeLightbox() {
    if (!lightbox) return;
    lightbox.classList.remove('active');
}

if (lbNext) lbNext.addEventListener('click', (e) => { e.stopPropagation(); showLightboxImage(lightboxIndex + 1); });
if (lbPrev) lbPrev.addEventListener('click', (e) => { e.stopPropagation(); showLightboxImage(lightboxIndex - 1); });
if (lbClose) lbClose.addEventListener('click', closeLightbox);

if (lightbox) {
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox || e.target.classList.contains('lightbox-img-wrapper')) closeLightbox();
    });
    
    let lbTouchStartX = 0;
    lightbox.addEventListener('touchstart', e => { lbTouchStartX = e.changedTouches[0].screenX; }, {passive: true});
    lightbox.addEventListener('touchend', e => {
        const diff = lbTouchStartX - e.changedTouches[0].screenX;
        if (Math.abs(diff) > 50) {
            if (diff > 0) showLightboxImage(lightboxIndex + 1);
            else showLightboxImage(lightboxIndex - 1);
        }
    });
}

// Global Keyboard Navigation
document.addEventListener('keydown', (e) => {
    const isEscape = e.key === 'Escape' || e.key === 'Esc' || e.keyCode === 27;
    const isRight = e.key === 'ArrowRight' || e.keyCode === 39;
    const isLeft = e.key === 'ArrowLeft' || e.keyCode === 37;

    if (lightbox && lightbox.classList.contains('active')) {
        if (isRight) showLightboxImage(lightboxIndex + 1);
        if (isLeft) showLightboxImage(lightboxIndex - 1);
        if (isEscape) closeLightbox();
    } else if (currentGalleryId) {
        if (isRight) updateGalleryCarousel(currentGalleryId, carouselIndexes[currentGalleryId] + 1);
        if (isLeft) updateGalleryCarousel(currentGalleryId, carouselIndexes[currentGalleryId] - 1);
        if (isEscape) closeGallery();
    }
});
