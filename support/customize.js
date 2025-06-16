if (localStorage.getItem('ideal-width')) {
    console.info('changing body width')
    document.documentElement.style.setProperty('--ideal',localStorage.getItem('ideal-width'))
    document.addEventListener('load',()=>setMediaWidths(localStorage.getItem('ideal-width')))
} else {
    document.addEventListener('load',()=>setMediaWidths(getComputedStyle(document.documentElement).getPropertyValue('--ideal')))
}
if (localStorage.getItem('font-size')) {
    console.info('changing font size')
    document.documentElement.style.setProperty('--fontsize',localStorage.getItem('font-size'))
}
if (localStorage.getItem('font-family')) {
    console.info('changing font family')
    document.documentElement.style.setProperty('--fontfamily',localStorage.getItem('font-family'))
}
function setIdealWidth(el) {
    if (!Number(el.value)) return
    let val = Number(el.value)
    if (val >= 100 || val <= 1) val = '100vw'
    else val = val + 'rem'
    document.documentElement.style.setProperty('--ideal', val)
    localStorage.setItem('ideal-width', val)
}
function setFontSize(el) {
    if (!Number(el.value)) return
    let val = Number(el.value) + 'rem'
    document.documentElement.style.setProperty('--fontsize', val)
    localStorage.setItem('font-size', val)
}
function setFontFamily(el) {
    let val = el.value.trim() || 'Palatino, Palladio URW, P052, TeX Gyre Pagella, Palatino Linotype, Book Antiqua, serif'
    document.documentElement.style.setProperty('--fontfamily', val)
    localStorage.setItem('font-family', val)
}
function setMediaWidths(width) {
    for(let sheet of document.styleSheets) {
        for(let rule of sheet.cssRules) {
            if (rule.media && /-width:/.test(rule.media.mediaText)) {
                rule.media.mediaText = rule.media.mediaText.replace(/-width: *([^;]*)/, '-width: '+width);
                console.info(rule.media.mediaText)
            }
        }
    }
}
window.addEventListener('load',e=>{
    if (localStorage.getItem('ideal-width')) {
        document.getElementById('in-width').value = localStorage.getItem('ideal-width').replace(/[^0-9.]/g, '')
    }
    if (localStorage.getItem('font-size')) {
        document.getElementById('in-size').value = localStorage.getItem('font-size').replace(/[^0-9.]/g, '')
    }
    if (localStorage.getItem('font-family')) {
        document.getElementById('in-font').value = localStorage.getItem('font-family')
    }
    let button=document.getElementById('restyle-button')
    let diag=document.getElementById('restyle-dialog')
    button.addEventListener('click', e => diag.showModal())
    
    document.querySelectorAll('.makefile').forEach(e=>e.innerHTML = e.innerHTML.replace(/    /g, '\t')) // makefile tabs
})
