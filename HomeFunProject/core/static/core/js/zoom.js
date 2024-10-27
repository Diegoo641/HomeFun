
  (function() {
    const maxZoom = 1; // 150%
    
    window.addEventListener('resize', function() {
        const scale = window.innerWidth / document.documentElement.clientWidth;
        
        if (scale > maxZoom) {
            document.body.style.transform = `scale(${maxZoom})`;
            document.body.style.transformOrigin = '0 0';
            document.body.style.width = `${document.documentElement.clientWidth / maxZoom}px`;
        } else {
            document.body.style.transform = '';
            document.body.style.width = '100%'; // Restablece el ancho
        }
    });
})();
