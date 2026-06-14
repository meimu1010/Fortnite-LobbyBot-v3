// Función para aplicar o actualizar pseudo-estilos
function applyPseudoStyle(id, css) {
    const styleId = id + '-pseudoStyle';
    let styleElement = document.getElementById(styleId);

    if (!styleElement) {
        styleElement = document.createElement('style');
        styleElement.id = styleId;
        document.head.appendChild(styleElement);
    }

    styleElement.innerHTML = css;
}

// Función para verificar si un pseudo-estilo existe con el mismo contenido CSS
function hasSameCSS(id, css) {
    const styleId = id + '-pseudoStyle';
    const styleElement = document.getElementById(styleId);

    return styleElement !== null && styleElement.innerHTML === css;
}