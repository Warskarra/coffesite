const learnMoreButton = document.getElementById("but");

function changeText() {
  if (!learnMoreButton) return;

  alert("Hello from external JavaScript!");
  learnMoreButton.textContent = "Thanks for checking!";
  learnMoreButton.style.color = "white";
}

if (learnMoreButton) {
  learnMoreButton.addEventListener("click", changeText);
}   

document.addEventListener('DOMContentLoaded', () => {

    const contactForm = document.querySelector('.contact-form form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const name = contactForm.querySelector('input[type="text"]').value;
          
            contactForm.innerHTML = `
                <div style="text-align: center; padding: 40px;">
                    <h2 style="color: #deab5f;">Thank you, ${name}!</h2>
                    <p>Your feedback has been sent successfully. We'll get back to you soon.</p>
                    <button onclick="location.reload()" style="margin-top: 20px;">Send another message</button>
                </div>
            `;
        });
    }

    const cartButtons = document.querySelectorAll('.product-card button');

    cartButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productName = button.parentElement.querySelector('h4').innerText;
            
            const originalText = button.innerText;
            button.innerText = "✓ Added to Cart";
            button.style.backgroundColor = "#27ae60"; // Green color
            
            console.log(`${productName} added to session cart.`);
            
            setTimeout(() => {
                button.innerText = originalText;
                button.style.backgroundColor = "#deab5f";
            }, 2000);
        });
    });

    const nav = document.querySelector('nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.style.backgroundColor = "rgba(0, 0, 0, 0.95)";
            nav.style.boxShadow = "0 2px 10px rgba(0,0,0,0.5)";
        } else {
            nav.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
            nav.style.boxShadow = "none";
        }
    });

});