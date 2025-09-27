// Divine Animations - Greek Goddess Enhanced Effects

class DivineAnimations {
    constructor() {
        this.initializeParticleSystem();
        this.initializeHoverEffects();
        this.initializeScrollAnimations();
        this.initializeDivineInteractions();
    }

    initializeParticleSystem() {
        // Create floating divine orbs
        this.createFloatingOrbs();

        // Create sparkle trails on mouse movement
        this.initializeSparkleTrail();
    }

    createFloatingOrbs() {
        const container = document.createElement('div');
        container.className = 'divine-orbs-container';
        container.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        `;

        for (let i = 0; i < 8; i++) {
            const orb = document.createElement('div');
            orb.className = 'divine-orb';
            orb.style.cssText = `
                position: absolute;
                width: ${Math.random() * 20 + 10}px;
                height: ${Math.random() * 20 + 10}px;
                background: radial-gradient(circle, rgba(212, 175, 55, 0.6) 0%, transparent 70%);
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: divine-float ${Math.random() * 10 + 15}s ease-in-out infinite;
                animation-delay: ${Math.random() * -10}s;
            `;
            container.appendChild(orb);
        }

        document.body.appendChild(container);

        // Add CSS for divine float animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes divine-float {
                0%, 100% {
                    transform: translateY(0) translateX(0) rotate(0deg);
                    opacity: 0.3;
                }
                25% {
                    transform: translateY(-100px) translateX(50px) rotate(90deg);
                    opacity: 0.8;
                }
                50% {
                    transform: translateY(-50px) translateX(-30px) rotate(180deg);
                    opacity: 0.6;
                }
                75% {
                    transform: translateY(-150px) translateX(80px) rotate(270deg);
                    opacity: 0.9;
                }
            }
        `;
        document.head.appendChild(style);
    }

    initializeSparkleTrail() {
        let mouseTrail = [];
        const maxTrailLength = 10;

        document.addEventListener('mousemove', (e) => {
            // Throttle the trail creation
            if (Math.random() > 0.7) {
                this.createSparkle(e.clientX, e.clientY);
            }

            // Update mouse trail for constellation effect
            mouseTrail.push({ x: e.clientX, y: e.clientY, time: Date.now() });

            if (mouseTrail.length > maxTrailLength) {
                mouseTrail.shift();
            }

            // Create constellation lines
            this.updateConstellation(mouseTrail);
        });
    }

    createSparkle(x, y) {
        const sparkle = document.createElement('div');
        sparkle.className = 'divine-sparkle';
        sparkle.style.cssText = `
            position: fixed;
            left: ${x}px;
            top: ${y}px;
            width: 4px;
            height: 4px;
            background: radial-gradient(circle, #FFD700 0%, transparent 100%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            animation: sparkle-fade 1s ease-out forwards;
        `;

        document.body.appendChild(sparkle);

        // Add sparkle animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes sparkle-fade {
                0% {
                    opacity: 1;
                    transform: scale(1) rotate(0deg);
                }
                100% {
                    opacity: 0;
                    transform: scale(0.3) rotate(180deg);
                }
            }
        `;
        document.head.appendChild(style);

        setTimeout(() => {
            if (sparkle.parentNode) {
                sparkle.parentNode.removeChild(sparkle);
            }
        }, 1000);
    }

    updateConstellation(trail) {
        // Remove existing constellation
        const existingConstellation = document.querySelector('.divine-constellation');
        if (existingConstellation) {
            existingConstellation.remove();
        }

        if (trail.length < 3) return;

        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.className = 'divine-constellation';
        svg.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9998;
        `;

        for (let i = 0; i < trail.length - 1; i++) {
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', trail[i].x);
            line.setAttribute('y1', trail[i].y);
            line.setAttribute('x2', trail[i + 1].x);
            line.setAttribute('y2', trail[i + 1].y);
            line.setAttribute('stroke', 'rgba(212, 175, 55, 0.3)');
            line.setAttribute('stroke-width', '1');
            line.style.opacity = (i / trail.length) * 0.5;
            svg.appendChild(line);
        }

        document.body.appendChild(svg);

        setTimeout(() => {
            if (svg.parentNode) {
                svg.parentNode.removeChild(svg);
            }
        }, 500);
    }

    initializeHoverEffects() {
        // Enhanced hover effects for interactive elements
        const interactiveElements = [
            '.divine-btn', '.nav-link', '.tool-card', '.source-card',
            '.creation-card', '.action-btn', '.upload-zone'
        ];

        interactiveElements.forEach(selector => {
            document.querySelectorAll(selector).forEach(element => {
                this.addDivineHoverEffect(element);
            });
        });
    }

    addDivineHoverEffect(element) {
        element.addEventListener('mouseenter', (e) => {
            // Create divine aura effect
            this.createDivineAura(e.target);

            // Add floating text effect
            this.createFloatingTitle(e.target);
        });

        element.addEventListener('mouseleave', (e) => {
            // Remove effects
            this.removeDivineEffects(e.target);
        });
    }

    createDivineAura(element) {
        const aura = document.createElement('div');
        aura.className = 'divine-aura-effect';
        aura.style.cssText = `
            position: absolute;
            top: -10px;
            left: -10px;
            right: -10px;
            bottom: -10px;
            background: radial-gradient(circle, rgba(212, 175, 55, 0.2) 0%, transparent 70%);
            border-radius: inherit;
            pointer-events: none;
            z-index: -1;
            animation: aura-pulse 2s ease-in-out infinite;
        `;

        element.style.position = 'relative';
        element.appendChild(aura);

        // Add aura pulse animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes aura-pulse {
                0%, 100% {
                    opacity: 0.3;
                    transform: scale(1);
                }
                50% {
                    opacity: 0.7;
                    transform: scale(1.1);
                }
            }
        `;
        document.head.appendChild(style);
    }

    createFloatingTitle(element) {
        const title = element.getAttribute('data-divine-title') ||
                     element.getAttribute('title') ||
                     element.textContent.trim().substring(0, 20);

        if (!title) return;

        const floatingText = document.createElement('div');
        floatingText.className = 'floating-divine-title';
        floatingText.textContent = title;
        floatingText.style.cssText = `
            position: absolute;
            top: -50px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(26, 22, 17, 0.95);
            color: var(--olympus-gold);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-family: var(--font-divine);
            font-size: 0.9rem;
            white-space: nowrap;
            z-index: 10000;
            border: 1px solid var(--olympus-gold);
            box-shadow: 0 4px 20px rgba(212, 175, 55, 0.4);
            animation: float-up 0.3s ease-out;
            pointer-events: none;
        `;

        element.appendChild(floatingText);

        // Add float animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float-up {
                0% {
                    opacity: 0;
                    transform: translateX(-50%) translateY(10px);
                }
                100% {
                    opacity: 1;
                    transform: translateX(-50%) translateY(0);
                }
            }
        `;
        document.head.appendChild(style);
    }

    removeDivineEffects(element) {
        const aura = element.querySelector('.divine-aura-effect');
        const title = element.querySelector('.floating-divine-title');

        if (aura) aura.remove();
        if (title) title.remove();
    }

    initializeScrollAnimations() {
        // Parallax scrolling effects
        window.addEventListener('scroll', () => {
            this.updateParallaxElements();
        });

        // Intersection Observer for element animations
        this.initializeIntersectionObserver();
    }

    updateParallaxElements() {
        const scrollY = window.pageYOffset;
        const particles = document.querySelector('.golden-particles');
        const columns = document.querySelector('.marble-columns');

        if (particles) {
            particles.style.transform = `translateY(${scrollY * 0.1}px) rotate(${scrollY * 0.02}deg)`;
        }

        if (columns) {
            columns.style.transform = `translateY(${scrollY * 0.05}px)`;
        }
    }

    initializeIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('divine-reveal');
                    this.animateElementEntrance(entry.target);
                }
            });
        }, observerOptions);

        // Observe elements for entrance animations
        const elementsToObserve = [
            '.tool-card', '.source-card', '.creation-card',
            '.upload-zone', '.source-options', '.chat-messages'
        ];

        elementsToObserve.forEach(selector => {
            document.querySelectorAll(selector).forEach(element => {
                observer.observe(element);
            });
        });
    }

    animateElementEntrance(element) {
        const animationType = element.getAttribute('data-animation') || 'fadeInUp';

        element.style.animation = `${animationType} 0.8s ease-out forwards`;

        // Add entrance animations CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fadeInUp {
                0% {
                    opacity: 0;
                    transform: translateY(30px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes slideInLeft {
                0% {
                    opacity: 0;
                    transform: translateX(-50px);
                }
                100% {
                    opacity: 1;
                    transform: translateX(0);
                }
            }

            @keyframes scaleIn {
                0% {
                    opacity: 0;
                    transform: scale(0.8);
                }
                100% {
                    opacity: 1;
                    transform: scale(1);
                }
            }
        `;
        document.head.appendChild(style);
    }

    initializeDivineInteractions() {
        // Add special click effects
        document.addEventListener('click', (e) => {
            this.createClickRipple(e);
        });

        // Add typing effect for divine messages
        this.initializeTypingEffects();

        // Add breath effect to important elements
        this.addBreathingEffect();
    }

    createClickRipple(e) {
        const ripple = document.createElement('div');
        ripple.className = 'divine-click-ripple';
        ripple.style.cssText = `
            position: fixed;
            left: ${e.clientX - 25}px;
            top: ${e.clientY - 25}px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(212, 175, 55, 0.6) 0%, transparent 70%);
            pointer-events: none;
            z-index: 9999;
            animation: ripple-expand 0.6s ease-out forwards;
        `;

        document.body.appendChild(ripple);

        // Add ripple animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes ripple-expand {
                0% {
                    opacity: 1;
                    transform: scale(0);
                }
                100% {
                    opacity: 0;
                    transform: scale(4);
                }
            }
        `;
        document.head.appendChild(style);

        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }

    initializeTypingEffects() {
        // Add typing effect to welcome messages
        const typingElements = document.querySelectorAll('[data-typing-effect]');

        typingElements.forEach(element => {
            this.typeText(element, element.textContent);
        });
    }

    typeText(element, text) {
        element.textContent = '';
        element.style.borderRight = '2px solid var(--olympus-gold)';

        let index = 0;
        const typeInterval = setInterval(() => {
            if (index < text.length) {
                element.textContent += text[index];
                index++;
            } else {
                clearInterval(typeInterval);
                // Remove cursor after typing
                setTimeout(() => {
                    element.style.borderRight = 'none';
                }, 1000);
            }
        }, 50);
    }

    addBreathingEffect() {
        const breathingElements = [
            '.athena-avatar', '.upload-icon', '.logo i'
        ];

        breathingElements.forEach(selector => {
            document.querySelectorAll(selector).forEach(element => {
                element.style.animation = 'divine-breathing 4s ease-in-out infinite';
            });
        });

        // Add breathing animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes divine-breathing {
                0%, 100% {
                    transform: scale(1);
                    filter: brightness(1);
                }
                50% {
                    transform: scale(1.05);
                    filter: brightness(1.2);
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Special method to create divine notifications
    showDivineNotification(message, type = 'divine') {
        const notification = document.createElement('div');
        notification.className = `divine-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-glow"></div>
            <div class="notification-content">
                <div class="notification-icon">✨</div>
                <span class="notification-text">${message}</span>
            </div>
        `;

        notification.style.cssText = `
            position: fixed;
            top: 120px;
            right: 20px;
            background: var(--temple-gradient);
            border: 2px solid var(--olympus-gold);
            border-radius: 20px;
            padding: 1.5rem;
            color: var(--marble-white);
            z-index: 10000;
            transform: translateX(400px);
            transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            max-width: 400px;
            box-shadow: var(--divine-shadow);
            backdrop-filter: blur(15px);
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Auto remove
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 500);
        }, 4000);
    }
}

// Initialize divine animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.divineAnimations = new DivineAnimations();

    // Add to global scope for other scripts to use
    window.showDivineNotification = (message, type) => {
        window.divineAnimations.showDivineNotification(message, type);
    };
});

// Add custom cursor effect
document.addEventListener('DOMContentLoaded', () => {
    const cursor = document.createElement('div');
    cursor.className = 'divine-cursor';
    cursor.style.cssText = `
        position: fixed;
        width: 20px;
        height: 20px;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.8) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
        z-index: 10001;
        mix-blend-mode: difference;
        transition: transform 0.1s ease;
    `;

    document.body.appendChild(cursor);

    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX - 10 + 'px';
        cursor.style.top = e.clientY - 10 + 'px';
    });

    // Scale cursor on interactive elements
    const interactiveSelectors = 'button, a, input, .tool-card, .source-card';

    document.addEventListener('mouseover', (e) => {
        if (e.target.matches(interactiveSelectors)) {
            cursor.style.transform = 'scale(2)';
        }
    });

    document.addEventListener('mouseout', (e) => {
        if (e.target.matches(interactiveSelectors)) {
            cursor.style.transform = 'scale(1)';
        }
    });
});