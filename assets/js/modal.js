(function() {
  var modal = document.getElementById('booking-modal');
  if (!modal) return;
  var closeBtn = document.getElementById('modal-close');
  var lastFocus;

  function openModal() {
    lastFocus = document.activeElement;
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }

  // Expose globally so inline onclick handlers can call openBookingModal()
  window.openBookingModal = openModal;

  closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', function(e) {
    if (e.target === modal) closeModal();
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal.style.display === 'flex') closeModal();
  });

  document.querySelectorAll('a[href="#form"].btn-red, a.header-cta[href="#form"], a[href="#contact"].btn-estimate').forEach(function(trigger) {
    trigger.addEventListener('click', function(e) {
      e.preventDefault();
      openModal();
    });
  });
})();
