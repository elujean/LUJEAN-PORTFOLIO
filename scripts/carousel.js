let currentSlide = 0;
let slides;

function openModal() {
  const modal = document.getElementById("hraModal");
  modal.classList.remove("hidden");
  modal.style.display = "flex";

  slides = document.querySelectorAll(".carousel-slide");
  currentSlide = 0;
  showSlide(currentSlide);
}

function closeModal() {
  const modal = document.getElementById("hraModal");
  modal.classList.add("hidden");
  modal.style.display = "none";
}

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.add("hidden");
    slide.classList.remove("active");
    if (i === index) {
      slide.classList.remove("hidden");
      slide.classList.add("active");
    }
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