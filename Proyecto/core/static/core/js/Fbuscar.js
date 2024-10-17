document.addEventListener("keyup", e=>{
  
  if (e.target.matches("#buscador")){
  
    if (e.key ==="Escape")e.target.value = ""

    document.querySelectorAll(".taller").forEach(taller =>{

        taller.textContent.toLowerCase().includes(e.target.value.toLowerCase())
          ?taller.classList.remove("filtro")
          :taller.classList.add("filtro")
    })
}
  })