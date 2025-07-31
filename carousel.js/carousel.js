let currentSlide = 0;
const slides = document.querySelectorAll('.carousel-slide');

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.toggle('hidden', i !== index);
    slide.classList.toggle('active', i === index);
  });
}

function nextSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide(currentSlide);
}

function prevSlide() {
  currentSlide = (currentSlide - 1 + slides.length) % slides.length;
  showSlide(currentSlide);
}

function openModal() {
  document.getElementById("hraModal").style.display = "flex";
  currentSlide = 0;
  showSlide(currentSlide);
}

function closeModal() {
  document.getElementById("hraModal").style.display = "none";
}