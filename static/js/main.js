document.addEventListener("DOMContentLoaded", function () {
  // ---------------- AOS ----------------
  if (window.AOS) {
    AOS.init({ duration: 700, once: true, offset: 60, easing: "ease-out-cubic" });
  }

  // ---------------- Navbar scroll state + mobile toggle ----------------
  const navbar = document.getElementById("navbar");
  const navToggle = document.getElementById("navToggle");
  const navLinks = document.getElementById("navLinks");

  window.addEventListener("scroll", function () {
    if (!navbar) return;
    navbar.classList.toggle("scrolled", window.scrollY > 40);
  });

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => navLinks.classList.toggle("open"));
    navLinks.querySelectorAll("a").forEach((link) =>
      link.addEventListener("click", () => navLinks.classList.remove("open"))
    );
  }

  // ---------------- Flash message dismiss ----------------
  document.querySelectorAll(".flash-close").forEach((btn) => {
    btn.addEventListener("click", () => btn.closest(".flash").remove());
  });
  setTimeout(() => {
    document.querySelectorAll(".flash").forEach((f) => f.remove());
  }, 6000);

  // ---------------- Typed.js hero role ----------------
  const typedTarget = document.getElementById("typed-role");
  if (typedTarget && window.Typed && window.HERO_TYPED_STRINGS) {
    new Typed("#typed-role", {
      strings: window.HERO_TYPED_STRINGS,
      typeSpeed: 45,
      backSpeed: 25,
      backDelay: 1400,
      loop: true,
    });
  }

  // ---------------- Skill bar fill on scroll ----------------
  const bars = document.querySelectorAll(".skill-bar-fill");
  if (bars.length) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            el.style.width = el.dataset.width + "%";
            observer.unobserve(el);
          }
        });
      },
      { threshold: 0.4 }
    );
    bars.forEach((bar) => observer.observe(bar));
  }

  // ---------------- Project filter ----------------
  const filterButtons = document.querySelectorAll(".filter-btn");
  const projectCards = document.querySelectorAll(".project-card");
  filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const filter = btn.dataset.filter;
      projectCards.forEach((card) => {
        const match = filter === "all" || card.dataset.category === filter;
        card.style.display = match ? "" : "none";
      });
    });
  });

  // ---------------- GSAP scroll-triggered section reveals ----------------
  if (window.gsap && window.ScrollTrigger) {
    gsap.registerPlugin(ScrollTrigger);
    gsap.utils.toArray(".section-head").forEach((head) => {
      gsap.from(head, {
        y: 30,
        opacity: 0,
        duration: 0.8,
        ease: "power2.out",
        scrollTrigger: { trigger: head, start: "top 85%" },
      });
    });
  }

  // ---------------- Three.js hero network (signature element) ----------------
  initHeroNetwork();
});

function initHeroNetwork() {
  const canvas = document.getElementById("hero-canvas");
  if (!canvas || !window.THREE || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    60,
    canvas.clientWidth / canvas.clientHeight || window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.z = 42;

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  const setSize = () => {
    const w = canvas.parentElement.clientWidth;
    const h = canvas.parentElement.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  setSize();
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // Node cloud representing a security/network graph
  const NODE_COUNT = 90;
  const nodes = [];
  const positions = new Float32Array(NODE_COUNT * 3);

  for (let i = 0; i < NODE_COUNT; i++) {
    const x = (Math.random() - 0.5) * 70;
    const y = (Math.random() - 0.5) * 40;
    const z = (Math.random() - 0.5) * 30;
    nodes.push(new THREE.Vector3(x, y, z));
    positions[i * 3] = x;
    positions[i * 3 + 1] = y;
    positions[i * 3 + 2] = z;
  }

  const pointsGeometry = new THREE.BufferGeometry();
  pointsGeometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  const pointsMaterial = new THREE.PointsMaterial({
    color: 0x7c5cfc,
    size: 0.9,
    transparent: true,
    opacity: 0.85,
  });
  const points = new THREE.Points(pointsGeometry, pointsMaterial);
  scene.add(points);

  // Connect nearby nodes with faint lines (network graph look)
  const lineVertices = [];
  const MAX_DIST = 13;
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      if (nodes[i].distanceTo(nodes[j]) < MAX_DIST) {
        lineVertices.push(nodes[i].x, nodes[i].y, nodes[i].z);
        lineVertices.push(nodes[j].x, nodes[j].y, nodes[j].z);
      }
    }
  }
  const lineGeometry = new THREE.BufferGeometry();
  lineGeometry.setAttribute("position", new THREE.BufferAttribute(new Float32Array(lineVertices), 3));
  const lineMaterial = new THREE.LineBasicMaterial({ color: 0x22d3ee, transparent: true, opacity: 0.12 });
  const lines = new THREE.LineSegments(lineGeometry, lineMaterial);
  scene.add(lines);

  const group = new THREE.Group();
  group.add(points);
  group.add(lines);
  scene.add(group);

  let mouseX = 0, mouseY = 0;
  window.addEventListener("mousemove", (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  function animate() {
    requestAnimationFrame(animate);
    group.rotation.y += 0.0012;
    group.rotation.x += (mouseY * 0.15 - group.rotation.x) * 0.02;
    group.rotation.y += (mouseX * 0.1) * 0.001;
    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener("resize", setSize);
}
