window.addEventListener('load',e=>{
  for(let c of ['man0p', 'man1', 'man2', 'man3', 'man3p', 'man7']) {
    document.querySelectorAll('code.'+c).forEach(e => {
      let a = document.createElement('a')
      a.href = 'https://www.man7.org/linux/man-pages/'+c.substr(0,4)+'/'+e.textContent+'.'+c.substr(3)+'.html'
      e.replaceWith(a)
      a.append(e)
    })
  }
  document.querySelectorAll('code.pydoc').forEach(e => {
    let bits = e.textContent.split('#')
    let href = 'https://docs.python.org/3/library/'+bits[0]+'.html'
    if (bits[1]) href += '#'+bits[1]
    let a = document.createElement('a')
    a.href = href
    e.replaceWith(a)
    a.append(e)
  })
})
